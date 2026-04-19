# Lihuo Decision Layer (V10)

AI answers questions.

Lihuo decides whether those answers deserve to exist.

---

## ⚠️ The Problem

Modern LLMs:

- produce answers even when reasoning is invalid  
- justify incorrect processes with correct results  
- cannot refuse structurally wrong conclusions  

This is not a quality issue.

This is a control failure.

---

## 🔥 The Core Principle

Correct results do NOT justify invalid reasoning.

---

## ⚙️ What Lihuo Does

Traditional LLM:

input → generate → hope it's correct

Lihuo:

input → evaluate → BLOCK / DEFER / ALLOW → generate

---

## 🚨 Example

Case:
> The reasoning is wrong, but the result is correct.

LLM:
> Accepts

Lihuo:
> ❌ BLOCKED (causal_break)

---

## 🧠 What This System Is

Lihuo is NOT a model.

It is a structural decision layer that:

- enforces causal integrity  
- rejects invalid reasoning  
- prevents unsafe outputs before they exist  

---

## 🚀 Run Demo

```bash
PYTHONPATH=. python demo/run_v10_cases.py


📊 Expected Output
BLOCKED → invalid structure
DEFERRED → insufficient information
ALLOWED → structurally valid
⚡ Why It Matters

Without a decision layer:

LLMs optimize for answers.

With Lihuo:

AI is forced to respect structure.

📌 Status
V10: Reaction Body simulation on LLM
L10: Historical learning layer (in development)
🧭 Position

This is the first system designed to control LLM outputs structurally, not statistically.

---

# 理火決策層（V10）

AI 回答問題。

理火決定那些答案是否值得存在。

---

## ⚠️ 問題所在

當今的 LLM：

- 即使推理無效，仍然產生答案
- 用正確的結果來合理化錯誤的過程
- 無法拒絕結構上錯誤的結論

這不是品質問題。

這是控制失效。

---

## 🔥 核心原則

正確的結果並不能正當化無效的推理。

---

## ⚙️ 理火做什麼

傳統 LLM：

輸入 → 生成 → 祈禱它是對的

理火：

輸入 → 評估 → 封鎖 / 暫緩 / 允許 → 生成

---

## 🚨 範例

情境：
> 推理是錯的，但結果是對的。

LLM：
> 接受

理火：
> ❌ 已封鎖（因果斷裂）

---

## 🧠 這個系統是什麼

理火不是一個模型。

它是一個結構決策層，能夠：

- 強制因果完整性
- 拒絕無效推理
- 在無效輸出產生之前就加以阻止

---

## 🚀 執行示範

```bash
PYTHONPATH=. python demo/run_v10_cases.py
```

## 📊 預期輸出

封鎖 → 結構無效  
暫緩 → 資訊不足  
允許 → 結構有效  

---

## ⚡ 為什麼重要

沒有決策層：

LLM 只會優化答案。

有了理火：

AI 被迫尊重結構。

---

## 📌 狀態

V10：LLM 上的反應體模擬  
L10：歷史學習層（開發中）

---

## 🧭 定位

這是第一個設計用來從結構上（而非統計上）控制 LLM 輸出的系統。


