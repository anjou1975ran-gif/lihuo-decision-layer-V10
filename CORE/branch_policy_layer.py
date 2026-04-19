# branch_policy_layer.py
BRANCH_POLICIES = {
    "causal": {
        "valid_claim": ["原因", "機制", "因果"],
        "fatal_error": ["missing_link", "因果鏈斷裂"],
        "stop_condition": ["因果成立"],
    },
    "structural": {
        "valid_claim": ["結構", "組成", "層級"],
        "fatal_error": ["fake_structure", "incomplete_structure"],
        "stop_condition": ["結構完整", "邊界清晰"],
    },
    "systemic": {
        "valid_claim": ["系統", "流程", "長期"],
        "fatal_error": ["memory_contamination", "global_damage"],
        "stop_condition": ["system-level failure", "局部最優"],
    },
}

class BranchPolicyLayer:
    def __init__(self):
        from CORE.reaction_body_engine_v1 import ReactionBodyEngine
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
