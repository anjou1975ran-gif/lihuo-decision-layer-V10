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


# ⚡ 理火決策層 — 示範

這個系統**不**回答問題。

它決定一個答案是否應該被允許存在。

---

## 🚀 執行

```bash
PYTHONPATH=. python demo/run_v10_cases.py
```

## 🧪 實際流程

每個案例會回傳：

**封鎖** → 已拒絕  
**暫緩** → 保留  
**允許** → 已許可  

---

## 🔥 關鍵測試

案例：

> 推理錯誤，結果正確

結果：

LLM → 接受  
理火 → ❌ 已封鎖  

---

## ⚠️ 重要

這個系統評估的是：

**推理結構**

而**不是**

**答案正確性**

---

## 🎯 意義

AI 不應該用答案來評判。

AI 應該用它產生答案的方式來評判。

---

## 👉 下一步

請參閱：

→ TESTER_GUIDE.md
