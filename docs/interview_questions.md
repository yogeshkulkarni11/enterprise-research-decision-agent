# Interview Questions

1. **Why use multiple agents?**
   Separate research, data, risk and decision responsibilities make the workflow easier to test, govern and extend.

2. **Where is RAG used?**
   The Research Agent retrieves enterprise policy evidence before the decision is made.

3. **Why combine RAG with SQL?**
   Policies provide qualitative constraints while structured data provides quantitative evidence.

4. **How is risk calculated?**
   The demo combines control scores and concentration exposure into a transparent risk score.

5. **How would you productionize it?**
   Replace local ChromaDB with Azure AI Search, SQLite with Azure SQL/Fabric, add Azure AI Foundry, Key Vault, identity, tracing, evaluation and human approval gates.

6. **Where should human-in-the-loop be added?**
   Before high-impact vendor approval, especially for high-risk or high-value contracts.

7. **What is the difference from a chatbot?**
   The system retrieves evidence, queries data, computes risk and makes a structured decision rather than only generating text.
