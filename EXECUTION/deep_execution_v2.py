from typing import Dict, Any, List


# =========================
# STEP 1：拆解問題
# =========================
def decompose_problem(user_input: str, llm) -> List[str]:
    prompt = f"""
請將以下問題拆解為 2~4 個「可推理的子問題」。

要求：
- 每個子問題要可獨立推理
- 不要重複
- 不要直接回答原問題

問題：
{user_input}
"""

    if llm is None:
        return ["(mock) 子問題1", "(mock) 子問題2"]

    response = llm(prompt, profile="deep")

    # 簡單切分（先用最粗暴版本）
    lines = [l.strip() for l in response.split("\n") if l.strip()]
    return lines[:4]


# =========================
# STEP 2：逐步推理
# =========================
def solve_steps(steps: List[str], llm) -> List[str]:
    results = []

    for step in steps:
        prompt = f"""
請對以下問題進行推理分析（不要只給結論）：

{step}
"""
        if llm is None:
            results.append(f"(mock solve) {step}")
        else:
            res = llm(prompt, profile="deep")
            results.append(res)

    return results


# =========================
# STEP 3：整合答案
# =========================
def synthesize_answer(user_input: str, steps: List[str], results: List[str], llm):
    prompt = f"""
你現在已完成多步推理。

請基於以下推理過程，整理出最終回答。

原問題：
{user_input}

子問題：
{steps}

推理結果：
{results}

要求：
- 保持邏輯一致
- 給出結論
- 不要忽略推理脈絡
"""

    if llm is None:
        return "(mock final answer)"

    return llm(prompt, profile="deep")


# =========================
# MAIN ENTRY
# =========================
def deep_execute(user_input: str,
                 semantic: Dict[str, Any],
                 decision: Dict[str, Any],
                 plan: Dict[str, Any],
                 llm):

    # ---------- STEP 1 ----------
    steps = decompose_problem(user_input, llm)

    # ---------- STEP 2 ----------
    results = solve_steps(steps, llm)

    # ---------- STEP 3 ----------
    final = synthesize_answer(user_input, steps, results, llm)

    # ---------- OUTPUT ----------
    return {
        "mode": "deep",
        "type": "multi_step_reasoning",
        "steps": steps,
        "intermediate_results": results,
        "final_answer": final
    }
