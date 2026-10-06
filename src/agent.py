from __future__ import annotations

import csv
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "data" / "documents"
DB_PATH = ROOT / "data" / "enterprise.db"


@dataclass
class ResearchEvidence:
    source: str
    text: str


class KnowledgeBase:
    def __init__(self):
        self.model = SentenceTransformer(os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))
        client = chromadb.PersistentClient(path=os.getenv("CHROMA_PATH", "./chroma_db"))
        self.collection = client.get_or_create_collection(os.getenv("CHROMA_COLLECTION", "enterprise_knowledge"))

    def index(self) -> int:
        docs, ids, metas = [], [], []
        for path in sorted(DOCS.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for i, section in enumerate(text.split("\n## ")):
                section = section.strip()
                if not section:
                    continue
                docs.append(section)
                ids.append(f"{path.stem}-{i}")
                metas.append({"source": path.name})
        if docs:
            embeddings = self.model.encode(docs).tolist()
            self.collection.upsert(ids=ids, documents=docs, embeddings=embeddings, metadatas=metas)
        return len(docs)

    def search(self, query: str, top_k: int = 4) -> list[ResearchEvidence]:
        embedding = self.model.encode([query]).tolist()
        result = self.collection.query(query_embeddings=embedding, n_results=top_k)
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        return [ResearchEvidence(m.get("source", "unknown"), d) for d, m in zip(docs, metas)]


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS vendors (
            vendor_id TEXT PRIMARY KEY, vendor_name TEXT, category TEXT,
            annual_cost_m REAL, security_score REAL, financial_score REAL,
            resilience_score REAL, regulatory_score REAL, concentration_pct REAL,
            implementation_months INTEGER)""")
        if con.execute("SELECT COUNT(*) FROM vendors").fetchone()[0] == 0:
            with open(ROOT / "data" / "vendors.csv", newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            con.executemany("INSERT INTO vendors VALUES (?,?,?,?,?,?,?,?,?,?)", [
                (r["vendor_id"], r["vendor_name"], r["category"], float(r["annual_cost_m"]),
                 float(r["security_score"]), float(r["financial_score"]), float(r["resilience_score"]),
                 float(r["regulatory_score"]), float(r["concentration_pct"]), int(r["implementation_months"]))
                for r in rows])


def data_agent(category: str) -> list[dict[str, Any]]:
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("SELECT * FROM vendors WHERE category = ? ORDER BY annual_cost_m", (category,)).fetchall()
        if not rows:
            rows = con.execute("SELECT * FROM vendors ORDER BY annual_cost_m").fetchall()
        return [dict(r) for r in rows]


def risk_agent(vendors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    assessed = []
    for v in vendors:
        avg_control = (v["security_score"] + v["financial_score"] + v["resilience_score"] + v["regulatory_score"]) / 4
        risk = (100 - avg_control) * 0.65 + min(v["concentration_pct"], 100) * 0.35
        band = "Low" if risk < 15 else "Medium" if risk < 25 else "High"
        assessed.append({**v, "risk_score": round(risk, 2), "risk_band": band})
    return assessed


def decision_agent(vendors: list[dict[str, Any]], evidence: list[ResearchEvidence]) -> dict[str, Any]:
    if not vendors:
        return {"decision": "No suitable vendor found", "rationale": [], "evidence": evidence}
    ranked = sorted(vendors, key=lambda v: (v["risk_score"], -v["security_score"], v["annual_cost_m"]))
    best = ranked[0]
    rationale = [
        f"Selected {best['vendor_name']} with risk score {best['risk_score']} ({best['risk_band']}).",
        f"Security score: {best['security_score']}; resilience score: {best['resilience_score']}; regulatory score: {best['regulatory_score']}.",
        f"Annual cost: ${best['annual_cost_m']:.2f}M and concentration: {best['concentration_pct']}%.",
    ]
    if best["risk_band"] == "High":
        rationale.append("High-risk selection requires Risk and Procurement approval before execution.")
    return {"decision": best["vendor_name"], "rationale": rationale, "alternatives": ranked[1:3], "evidence": evidence}


def run_decision(category: str = "Cloud") -> dict[str, Any]:
    kb = KnowledgeBase()
    kb.index()
    evidence = kb.search(f"vendor risk security procurement policy for {category}")
    vendors = risk_agent(data_agent(category))
    return decision_agent(vendors, evidence)
