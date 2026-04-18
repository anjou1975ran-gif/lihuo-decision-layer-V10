from typing import Dict, Any, List


# =========================
# STEP 1：拆解
# =========================
def decompose_problem(user_input: str, llm) -> List[str]:
    prompt = f"""
請將問題拆解為 2~4 個可推理的子問題：
- 不重複
- 可獨立推理
- 不要直接回答

問題：
{user_input}
"""
    if llm is None:
        return ["(mock) 子問題1", "(mock) 子問題2"]

    resp = llm(prompt, profile="deep")
    lines = [l.strip("-• ").strip() for l in resp.split("\n") if l.strip()]
    return lines[:4] if lines else [user_input]


# =========================
# STEP 2：單輪推理
# =========================
def solve_once(steps: List[str], llm) -> List[str]:
    results = []
    for s in steps:
        prompt = f"""
請對以下問題進行推理分析（說明推理過程）：
{s}
"""
        if llm is None:
            results.append(f"(mock solve) {s}")
        else:
            results.append(llm(prompt, profile="deep"))
    return results


# =========================
# STEP 3：整合
# =========================
def synthesize(user_input: str, steps: List[str], results: List[str], llm):
    prompt = f"""
基於以下多步推理，給出最終回答：

原問題：
{user_input}

子問題：
{steps}

推理結果：
{results}

要求：
- 邏輯一致
- 有結論
- 不忽略推理脈絡
"""
    if llm is None:
        return "(mock final answer)"
    return llm(prompt, profile="deep")


# =========================
# STEP 4：自我檢查（關鍵）
# =========================
def self_check(user_input: str, draft_answer: str, llm) -> Dict[str, Any]:
    prompt = f"""
請檢查以下回答是否存在問題：

原問題：
{user_input}

回答：
{draft_answer}

請輸出：
1. 是否合理（yes/no）
2. 是否有邏輯漏洞（簡述）
3. 是否需要再推理（yes/no）
"""
    if llm is None:
        return {"ok": True, "need_refine": False, "note": "(mock)"}

    resp = llm(prompt, profile="deep")

    text = resp.lower()
    need_refine = ("no" in text and "是否合理" in resp) or ("need" in text)
    ok = not need_refine

    return {
        "ok": ok,
        "need_refine": need_refine,
        "raw": resp
    }


# =========================
# MAIN LOOP
# =========================
def deep_execute(user_input: str,
                 semantic: Dict[str, Any],
                 decision: Dict[str, Any],
                 plan: Dict[str, Any],
                 llm,
                 max_iters: int = 3):

    history = []
    steps = decompose_problem(user_input, llm)

    current_answer = None

    for i in range(max_iters):
        # ---- solve ----
        results = solve_once(steps, llm)

        # ---- synthesize ----
        current_answer = synthesize(user_input, steps, results, llm)

        # ---- self-check ----
        check = self_check(user_input, current_answer, llm)

        history.append({
            "iteration": i + 1,
            "steps": steps,
            "results": results,
            "answer": current_answer,
            "check": check
        })

        # ---- stop condition ----
        if check["ok"] and not check["need_refine"]:
            break

        # ---- refine strategy（簡單版）----
        steps = [
            f"{s}（請修正前一次推理中的問題）"
            for s in steps
        ]

    return {
        "mode": "deep",
        "type": "iterative_reasoning",
        "iterations": len(history),
        "history": history,
        "final_answer": current_answer
    }
