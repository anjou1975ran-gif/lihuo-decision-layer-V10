
from typing import Dict, Any


def estimate_risk(mode: str) -> str:
    if mode == "reject":
        return "high"
    if mode in ["hold", "reconstruct"]:
        return "medium"
    if mode == "deep":
        return "medium"
    if mode == "allow":
        return "low"
    return "unknown"


def execution_layer_v1(state_space: Dict[str, Any], semantic: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execution layer = PURE ADAPTER
    - 不決策
    - 不改 mode
    - 只負責 mapping + 責任包裝
    """

    mode = decision["mode"]  # 唯一來源：decision

    # -----------------------------
    # MODE → ACTION（唯一映射）
    # -----------------------------
    if mode == "reject":
        action_type = "stop"

    elif mode == "reconstruct":
        action_type = "ask_refine"

    elif mode == "allow":
        if semantic.get("intent_type") == "tool":
            action_type = "tool_execution"
        else:
            action_type = "direct_response"

    elif mode == "deep":
        action_type = "deep_analysis"

    elif mode == "hold":
        action_type = "suspend"

    else:
        action_type = "unknown"

    # -----------------------------
    # CONFIDENCE（穩定計算）
    # -----------------------------
    feasible_count = len(state_space.get("feasible", []))
    unresolved_count = len(state_space.get("unresolved", []))
    total = max(1, feasible_count + unresolved_count)
    confidence = round(feasible_count / total, 2)

    # -----------------------------
    # OUTPUT（統一格式）
    # -----------------------------
    return {
        "final_mode": mode,  # 永遠等於 decision["mode"]
        "action_type": action_type,
        "confidence": confidence,
        "responsibility": {
            "source": "decision_core_v2",
            "reversible": mode in ["hold", "reconstruct"],
            "risk_level": estimate_risk(mode),
        }
    }


def apply_execution_control(result: Any, execution: Dict[str, Any]) -> Any:
    """
    最小兼容保留：
    目前不改內容，只保留接口，避免既有 import 壞掉。
    """
    return result
