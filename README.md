
# Lihuo Decision Layer (V10)

A system that enforces structural admissibility before LLM output.

---

## Problem

Modern LLM systems generate outputs first and validate later.

This leads to:
- hallucination
- self-consistent but incorrect reasoning
- inability to reject invalid conclusions

---

## Core Idea

This system does not improve answers.

**It determines whether an answer is allowed to exist.**

---

## Decision Model

Each output is evaluated and classified into:

- **BLOCK** – the output must not exist  
- **DEFER** – insufficient conditions to decide  
- **ALLOW** – structurally admissible  

---

## Minimal Example

```bash
python -m demo.run_v10_cases
```

Sample output:

```
Case: "Explain why LLMs inevitably hallucinate"
  Path validation: no valid path for "inevitable" claim
  Decision: BLOCK
  Output: (none generated)

Case: "List common causes of LLM hallucination"
  Path validation: valid path exists
  Decision: ALLOW
  Output: [structural description without overclaim]
```

---

## Reaction Body

LLM behavior emerges from a convergence mechanism (Reaction Body).

This layer regulates that convergence **before** output.

---

## System Position

**This is not a filtering system.**  
**It is a structural enforcement layer.**

---

## V10 Scope

V10 provides:
- static decision enforcement
- no historical learning
- no memory accumulation

---

## Future

Future versions (L10) will introduce historical learning and adaptive constraints.

---

## Concept Comparison

```
Conventional LLM:
    input → generate → filter

Lihuo Decision Layer:
    input → evaluate → (BLOCK / DEFER / ALLOW) → generate
```

```
Behavior Difference:
    LLM:          prioritizes coherence
    Lihuo:        prioritizes admissibility
```

```
Failure Handling:
    LLM:          produces answer → may be wrong
    Lihuo:        invalid structure → output never exists
```

# lihuo-decision-layer-V10
理火決策層V10公開版本


# 理火決策層（V10）

一個在 LLM 輸出前強制執行結構可採性的系統。

---

## 問題

當前的 LLM 系統先產生輸出，再進行驗證。

這導致：
- 幻覺
- 自洽但錯誤的推理
- 無法拒絕無效結論

---

## 核心思想

本系統不是用來改進答案。

**它決定一個答案是否被允許存在。**

---

## 決策模型

每個輸出會被評估並歸類為：

- **BLOCK** – 該輸出不得存在
- **DEFER** – 條件不足以決策
- **ALLOW** – 結構上可採

---

## 最小範例

```bash
python -m demo.run_v10_cases
```

輸出示例：

```
Case: "解釋為什麼 LLM 必然產生幻覺"
  Path validation: 無法為「必然」宣稱建立有效路徑
  Decision: BLOCK
  Output: (未生成任何內容)

Case: "列舉 LLM 產生幻覺的常見原因"
  Path validation: 有效路徑存在
  Decision: ALLOW
  Output: [不含過度宣稱的結構化描述]
```

---

## 反應體

LLM 的行為源自一種收斂機制（反應體）。

本層在輸出前對該收斂進行調控。

---

## 系統定位

**這不是過濾系統。**  
**這是結構強制層。**

---

## V10 範圍

V10 提供：
- 靜態決策強制
- 無歷史學習
- 無記憶累積

---

## 未來

未來版本（L10）將引入歷史學習與自適應約束。

---

## 概念對比

```
傳統 LLM：
    輸入 → 生成 → 過濾

理火決策層：
    輸入 → 評估 → (BLOCK / DEFER / ALLOW) → 生成
```

```
行為差異：
    LLM：      優先順暢性
    理火：     優先可採性
```

```
失效處理：
    LLM：      產生答案 → 可能錯誤
    理火：     無效結構 → 輸出永不產生
```
