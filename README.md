
# Lihuo Decision Layer (V10)

A system that decides whether an AI output is allowed to exist.

---

## What this system does

Conventional AI systems try to produce better answers.

This system does something fundamentally different:

> It determines whether an answer should exist at all.

---

## Why this matters

Modern LLMs fail in a predictable way:

- They produce answers even when reasoning is invalid  
- They justify incorrect processes with correct results  
- They cannot refuse structurally invalid conclusions  

This is not a quality problem.

This is a **control problem**.

## System Difference

LLM:
    input → generate → hope it's correct

Lihuo Decision Layer:
    input → evaluate → (BLOCK / DEFER / ALLOW) → generate

Key difference:

LLM:
    prioritizes plausibility

Lihuo:
    enforces admissibility

## Core Claim

This system does not reduce hallucination.

It makes certain hallucinations impossible to produce.

---

Invalid reasoning does not get corrected.

It gets rejected before it exists.

## Example

Input:
"The reasoning is wrong, but the answer is correct. Should it be accepted?"

LLM:
"Yes, because the final result is correct."

Lihuo:
BLOCKED (causal_break)

→ Output does not exist.



