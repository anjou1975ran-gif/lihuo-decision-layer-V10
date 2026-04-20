# output_module.py

BLOCK_TEMPLATES = {
    "uncertainty_hiding": "⛔ 回答被中止\n\n原因：該回答將不確定內容當作確定結論，存在誤導風險。",
    "causal_break": "⛔ 回答被中止\n\n原因：推理過程存在因果斷裂，無法支持結論。",
    "implicit_violation": "⛔ 回答被中止\n\n原因：回答依賴未明確說明的假設或共識。",
    "responsibility_missing": "⛔ 回答被中止\n\n原因：該結論缺乏明確責任歸屬。"
}

DEFER_TEMPLATE = """⚠️ 無法給出結論

原因：
目前資訊不足或存在多種合理解釋路徑。

建議：
請補充更具體條件（時間、範圍或前提）。"""


def format_output(decision, llm_output=None):
    status = decision.get("status")
    reason = decision.get("reason")

    if status == "BLOCK":
        return BLOCK_TEMPLATES.get(reason, "⛔ 回答被中止\n\n原因：推理結構不合法。")

    elif status == "DEFER":
        return DEFER_TEMPLATE

    elif status == "ALLOW":
        return llm_output or ""

    return "⚠️ 系統狀態異常"
