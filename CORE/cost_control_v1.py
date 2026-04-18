from typing import Dict, Any


def cost_control_v1(semantic: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decide whether deep is worth doing, and how many iterations are allowed.
    """

    intent = semantic.get("intent_type", "unknown")
    depth = float(semantic.get("semantic_depth", 0.0))
    memory_hint = semantic.get("memory_hint", "neutral")
    mode = decision.get("mode", "allow")

    # default
    allow_deep = mode == "deep"
    max_iters = 1
    cost_level = "low"
    reason = "default"

    if mode != "deep":
        return {
            "allow_deep": False,
            "max_iters": 0,
            "cost_level": "none",
            "reason": "mode_not_deep",
        }

    # ---- high depth reasoning / structure ----
    if intent in ["structure", "reasoning"]:
        if depth >= 0.9:
            max_iters = 3
            cost_level = "high"
            reason = "very_high_depth_reasoning"
        elif depth >= 0.75:
            max_iters = 2
            cost_level = "medium"
            reason = "high_depth_reasoning"
        else:
            max_iters = 1
            cost_level = "low"
            reason = "borderline_deep"

    # ---- boundary should almost never deep ----
    elif intent == "boundary":
        allow_deep = False
        max_iters = 0
        cost_level = "none"
        reason = "boundary_should_hold"

    else:
        max_iters = 1
        cost_level = "low"
        reason = "non_core_intent"

    # ---- memory effect ----
    if memory_hint == "prefer_deep":
        if max_iters < 3:
            max_iters += 1
        if cost_level == "low":
            cost_level = "medium"

    elif memory_hint == "avoid_deep":
        if depth < 0.85:
            allow_deep = False
            max_iters = 0
            cost_level = "none"
            reason = "memory_avoid_deep"

    return {
        "allow_deep": allow_deep,
        "max_iters": max_iters,
        "cost_level": cost_level,
        "reason": reason,
    }
