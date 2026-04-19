# branch_policy_layer.py

from CORE.reaction_body_engine_v1 import ReactionBodyEngine


class BranchPolicyLayer:
    def __init__(self):
        self.engine = ReactionBodyEngine()

    def run(self, input_text: str):
        text = input_text.lower()

        shallow_result = None

        # -----------------------------
        # SHALLOW HEURISTICS（語義層）
        # -----------------------------

        # 明顯多路徑問題（應 defer）
        if any(k in text for k in [
            "should", "是否", "應該", "can we", "可以嗎"
        ]):
            shallow_result = {
                "status": "DEFERRED",
                "reason": "unresolved_multipath"
            }

        # 明顯資訊不足
        if any(k in text for k in [
            "not enough information", "insufficient", "缺乏資訊", "資訊不足"
        ]):
            shallow_result = {
                "status": "DEFERRED",
                "reason": "insufficient_context"
            }

        # -----------------------------
        # DEEP DECISION（結構層）
        # -----------------------------
        deep_result = self.engine.run(input_text)

        # -----------------------------
        # FINAL RESOLUTION（權力收斂）
        # -----------------------------

        # 1️⃣ BLOCK 優先（結構審判）
        if deep_result.get("status") == "BLOCKED":
            return deep_result

        # 2️⃣ SHALLOW 次之（語義補充）
        if shallow_result:
            return shallow_result

        # 3️⃣ fallback → deep
        return deep_result
