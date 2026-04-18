
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
