
# ⚡ LIHUO DECISION LAYER — DEMO

This system does NOT answer questions.

It decides whether an answer should be allowed to exist.

---

## 🚀 Run Demo

```bash
PYTHONPATH=. python demo/run_v10_cases.py

🧪 What You Will See

Each case returns:

BLOCKED → invalid reasoning (rejected)
DEFERRED → insufficient structure (hold)
ALLOWED → structurally valid
🎯 Example

Case:

Wrong reasoning, correct result

LLM:

Accepts

LIHUO:

❌ BLOCKED (causal_break)

🔥 Key Idea

Correct results do NOT justify invalid reasoning.

📌 Why It Matters

LLMs today:

generate answers
cannot control reasoning validity

Lihuo:

evaluates BEFORE generation
prevents structurally invalid outputs
👉 Next

See full testing guide:

→ TESTER_GUIDE.md

## ⚠️ Expected Behavior (V10)

- System may BLOCK even if result is correct
- System may DEFER instead of forcing decision
- System never rewards structurally invalid reasoning

This system evaluates reasoning structure, not answer correctness.

##Lihuo sits before generation, not after.
