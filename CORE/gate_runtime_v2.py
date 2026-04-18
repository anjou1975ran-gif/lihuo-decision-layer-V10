from typing import Dict, Any


def gate_runtime_v2(semantic: Dict[str, Any], decision: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gate:
    - 只控制 allow_execution
    - 不改 mode
    """
    mode = decision["mode"]

    # -----------------------------
    # HARD BLOCK（不可逆）
    # -----------------------------
    if mode == "reject":
        return {
            "allow_execution": False,
            "runtime_action": "stop"
        }

    # -----------------------------
    # HOLD（暫停）
    # -----------------------------
    if mode == "hold":
        return {
            "allow_execution": False,
            "runtime_action": "wait"
        }

    # -----------------------------
    # RECONSTRUCT（需要補資料）
    # -----------------------------
    if mode == "reconstruct":
        return {
            "allow_execution": False,
            "runtime_action": "ask"
        }

    # -----------------------------
    # ALLOW / DEEP（允許執行）
    # -----------------------------
    if mode in ["allow", "deep"]:
        return {
            "allow_execution": True,
            "runtime_action": "execute"
        }

    # -----------------------------
    # DEFAULT（保守）
    # -----------------------------
    return {
        "allow_execution": False,
        "runtime_action": "wait"
    }
