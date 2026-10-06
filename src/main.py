from .agent import run_decision


if __name__ == "__main__":
    result = run_decision("Cloud")
    print(f"Recommended vendor: {result['decision']}")
    for item in result["rationale"]:
        print(f"- {item}")
    print("\nEvidence:")
    for evidence in result["evidence"]:
        print(f"- {evidence.source}: {evidence.text[:180]}...")
