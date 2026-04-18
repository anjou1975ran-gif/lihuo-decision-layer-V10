from typing import Dict, Any, List


def failure_detector_v1(history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detect whether deep reasoning is degrading, stalling, or no longer worth continuing.

    history item example:
    {
        "iteration": 1,
        "confidence": 0.72,
        "answer": "...",
        "self_check": "ok"
    }
    """

    if not history:
        return {
            "failure_risk": "low",
            "should_stop": False,
            "reason": "no_history",
        }

    if len(history) == 1:
        return {
            "failure_risk": "low",
            "should_stop": False,
            "reason": "insufficient_history",
        }

    last = history[-1]
    prev = history[-2]

    last_conf = float(last.get("confidence", 0.0))
    prev_conf = float(prev.get("confidence", 0.0))

    last_answer = str(last.get("answer", "")).strip()
    prev_answer = str(prev.get("answer", "")).strip()

    # ---- case 1: confidence falling ----
    if last_conf + 0.08 < prev_conf:
        return {
            "failure_risk": "high",
            "should_stop": True,
            "reason": "confidence_drop",
        }

    # ---- case 2: answer nearly unchanged ----
    if last_answer and prev_answer:
        overlap = _overlap_ratio(last_answer, prev_answer)
        if overlap > 0.9:
            return {
                "failure_risk": "medium",
                "should_stop": True,
                "reason": "answer_stagnation",
            }

    # ---- case 3: self-check explicitly weak ----
    if str(last.get("self_check", "")).lower() in ["weak", "uncertain", "degrading"]:
        return {
            "failure_risk": "high",
            "should_stop": True,
            "reason": "self_check_negative",
        }

    return {
        "failure_risk": "low",
        "should_stop": False,
        "reason": "continue",
    }


def _overlap_ratio(a: str, b: str) -> float:
    sa = set(a.split())
    sb = set(b.split())

    if not sa or not sb:
        return 0.0

    return len(sa & sb) / max(len(sa), len(sb))
