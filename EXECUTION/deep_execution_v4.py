from typing import Dict, Any, List


# =========================
# CONFIDENCE 評估（核心）
# =========================
def evaluate_confidence(answer: str, llm) -> float:
    prompt = f"""
請評估以下回答的品質（0~1）：

評估標準：
- 邏輯一致性
- 是否完整回答問題
- 是否有明顯漏洞

回答：
{answer}

只輸出一個數字（例如：0.75）
"""

    if llm is None:
        return 0.7

    resp = llm(prompt, profile="deep")

    try:
        return float(resp.strip())
    except:
        return 0.5


# =========================
# SELF CHECK（沿用）
# =========================
def self_check(user_input: str, answer: str, llm):
    prompt = f"""
檢查以下回答是否有問題：

問題：
{user_input}

回答：
{answer}

請回答：
1. 是否合理（yes/no）
2. 是否需要改進（yes/no）
"""

    if llm is None:
        return {"ok": True, "refine": False}

    resp = llm(prompt, profile="deep").lower()

    return {
        "ok": "yes" in resp,
        "refine": "no" not in resp
    }


# =========================
# MAIN LOOP（收斂控制）
# =========================
def deep_execute(user_input: str,
                 semantic: Dict[str, Any],
                 decision: Dict[str, Any],
                 plan: Dict[str, Any],
                 llm,
                 max_iters: int = 5,
                 confidence_threshold: float = 0.75):

    history = []
    best_answer = None
    best_score = 0.0

    steps = [user_input]  # 初始簡化（不再拆太細）

    for i in range(max_iters):

        # ---- 推理 ----
        prompt = f"""
請深入分析並回答：

{user_input}

要求：
- 展開推理
- 避免直接結論
"""
        answer = llm(prompt, profile="deep") if llm else "(mock answer)"

        # ---- 評分 ----
        confidence = evaluate_confidence(answer, llm)

        # ---- 自檢 ----
        check = self_check(user_input, answer, llm)

        # ---- 記錄 ----
        history.append({
            "iteration": i + 1,
            "answer": answer,
            "confidence": confidence,
            "check": check
        })

        # ---- 更新最佳 ----
        if confidence > best_score:
            best_score = confidence
            best_answer = answer

        # 🔥 提前停止條件
        if confidence >= confidence_threshold and check["ok"]:
            break

        # 🔥 如果開始退化 → 停
        if i > 1 and confidence < best_score:
            break

    return {
        "mode": "deep",
        "type": "iterative_reasoning_v2",
        "iterations": len(history),
        "best_confidence": round(best_score, 2),
        "history": history,
        "final_answer": best_answer
    }
