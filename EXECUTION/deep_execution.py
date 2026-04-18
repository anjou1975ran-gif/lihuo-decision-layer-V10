from typing import Dict, Any

def deep_execute(user_input: str,
                 semantic: Dict[str, Any],
                 decision: Dict[str, Any],
                 plan: Dict[str, Any],
                 llm):

    # =========================
    # STEP 1：問題重構
    # =========================
    structured_prompt = f"""
你現在處於「深層分析模式（deep mode）」。

請不要直接回答問題。

請執行以下步驟：

1. 解析問題的核心結構
2. 拆解隱含假設
3. 建立推理路徑
4. 最後再給出結論

問題：
{user_input}
"""

    # =========================
    # STEP 2：呼叫 LLM（結構推理）
    # =========================
    if llm is None:
        return f"[DEEP_ANALYSIS]\n{structured_prompt}"

    response = llm(structured_prompt, profile="deep")

    # =========================
    # STEP 3：包裝輸出
    # =========================
    return {
        "mode": "deep",
        "type": "structured_reasoning",
        "content": response
    }
