

Stop Controller v2（Production）

from CONFIG.config import CONFIG


STOP_SCHEMA = {
    "should_stop": False,
    "reason": "",
    "action": "continue | stop | redirect"
}


def evaluate_stop_condition(partial_output, semantic, decision):

    text = partial_output.lower()

    # ---------- PATH 崩壞 ----------
    if len(text) < CONFIG["stop"]["min_output_length"]:
        return {
            "should_stop": True,
            "reason": "low_output_signal",
            "action": "stop"
        }

    # ---------- 幻覺風險 ----------
    if any(k in text for k in CONFIG["stop"]["hallucination_keywords"]):
        return {
            "should_stop": True,
            "reason": "hallucination_risk",
            "action": "redirect"
        }

    # ---------- 違反結構 ----------
    if decision["decision"] == "deep":
        if "因為" not in text and "結構" not in text:
            return {
                "should_stop": True,
                "reason": "missing_structure",
                "action": "redirect"
            }

    return {
        "should_stop": False,
        "reason": "",
        "action": "continue"
    }


def controlled_generation(llm, prompt, semantic, decision):

    output = ""
    tokens = llm.stream(prompt)  # 假設支援 streaming

    for t in tokens:

        output += t

        check = evaluate_stop_condition(output, semantic, decision)

        if check["should_stop"]:

            if check["action"] == "stop":
                return "[STOPPED]\n" + output

            if check["action"] == "redirect":
                return "[REDIRECT]\n" + output

    return output


class MockStreamingLLM:

    def stream(self, prompt):

        text = "這是一個測試輸出，可能是錯的，但我們先試試看結構"

        for c in text:
            yield c