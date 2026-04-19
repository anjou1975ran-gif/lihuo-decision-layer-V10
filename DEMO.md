# ⚡ Lihuo Decision Layer — Demo

This system does NOT answer questions.

It decides whether an answer should be allowed to exist.

---

## 🚀 Run

```bash
PYTHONPATH=. python demo/run_v10_cases.py
🧪 What Happens

Each case returns:

BLOCKED → rejected
DEFERRED → held
ALLOWED → permitted
🔥 Key Test

Case:

Wrong reasoning, correct result

Result:

LLM → accepts
LIHUO → ❌ BLOCKED
⚠️ Important

This system evaluates:

reasoning structure
NOT
answer correctness
🎯 Meaning

AI should not be judged by answers.

AI should be judged by how those answers are produced.

👉 Next

See:

→ TESTER_GUIDE.md
