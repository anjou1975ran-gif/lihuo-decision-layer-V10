
from typing import Dict, Any, List

from CORE.cost_control_v1 import cost_control_v1
from CORE.failure_detector_v1 import failure_detector_v1


def deep_execute(user_input: str, semantic: Dict[str, Any], decision: Dict[str, Any], plan: Dict[str, Any], llm):

    cost = cost_control_v1(semantic, decision)

    if not cost["allow_deep"]:
        return {
            "type": "deep_skipped",
            "action_type": "direct_response",
            "best_confidence": 0.55,
            "iterations": 0,
            "final_answer": f"[SKIP_DEEP:{cost['reason']}] {user_input}",
            "history": [],
            "cost": cost,
        }

    max_iters = cost["max_iters"]
    history: List[Dict[str, Any]] = []

    best_answer = ""
    best_conf = 0.0

    for i in range(max_iters):

        answer = _run_single_deep_step(user_input, i + 1, llm)
        confidence = _estimate_confidence(user_input, answer, semantic, i + 1)
        self_check = _self_check(answer, confidence)

        step = {
            "iteration": i + 1,
            "answer": answer,
            "confidence": confidence,
            "self_check": self_check,
        }
        history.append(step)

        if confidence > best_conf:
            best_conf = confidence
            best_answer = answer

        failure = failure_detector_v1(history)
        if failure["should_stop"]:
            return {
                "type": "deep_analysis",
                "action_type": "deep_analysis",
                "best_confidence": round(best_conf, 3),
                "iterations": i + 1,
                "final_answer": best_answer,
                "history": history,
                "cost": cost,
                "failure": failure,
            }

    return {
        "type": "deep_analysis",
        "action_type": "deep_analysis",
        "best_confidence": round(best_conf, 3),
        "iterations": len(history),
        "final_answer": best_answer,
        "history": history,
        "cost": cost,
        "failure": {
            "failure_risk": "low",
            "should_stop": False,
            "reason": "completed_max_iters",
        },
    }
