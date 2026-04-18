from typing import Dict, Any


def select_llm_profile(mode: str) -> str:
    if mode == "deep":
        return "deep"
    if mode == "allow":
        return "surface"
    return "none"


def build_preprocess(mode: str, semantic: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "normalize": True,
        "intent_type": semantic.get("intent_type"),
        "structure_type": semantic.get("structure_type"),
        "mode": mode,
    }


def determine_final_action(mode: str) -> str:
    if mode == "reject":
        return "stop"
    if mode == "reconstruct":
        return "clarify"
    if mode == "hold":
        return "wait"
    return "respond"


def build_state_update(mode: str) -> Dict[str, Any]:
    return {
        "record_mode": mode,
        "pending": mode in ["hold", "reconstruct"],
    }


def orchestrator_v2(user_input: str, semantic: Dict[str, Any], decision: Dict[str, Any], state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Orchestrator = build plan only
    - 不重新決策 mode
    - 不 fallback 到 allow
    """
    mode = decision["mode"]

    llm_call = mode in ["allow", "deep"]

    plan = {
        "execution_mode": mode,
        "llm_call": llm_call,
        "llm_profile": select_llm_profile(mode),
        "boundary_prompt": "",
        "preprocess": build_preprocess(mode, semantic),
        "postprocess": [],
        "state_update": build_state_update(mode),
        "final_action": determine_final_action(mode),
    }

    return plan
