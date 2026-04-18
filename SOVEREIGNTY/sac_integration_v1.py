
---

#SAC Integration v1（Production）


from CONFIG.config import CONFIG


def sac_evaluate(semantic, decision, plan, state):

    # ---------- 張力 ----------
    tension = 0.0

    if semantic["intent_type"] in ["structure", "boundary"]:
        tension += 0.4

    if semantic["structure_type"] == "recursive":
        tension += 0.3

    # ---------- 不一致 ----------
    if (
        decision["decision"] == "allow"
        and semantic["semantic_depth"] > CONFIG["sac"]["high_tension_depth"]
    ):
        return {
            "override": True,
            "new_decision": "deep",
            "reason": "high_tension_not_expanded"
        }

    # ---------- 過度拒絕 ----------
    if (
        decision["decision"] == "reject"
        and tension < CONFIG["sac"]["min_tension_for_deep"]
    ):
        return {
            "override": True,
            "new_decision": "reconstruct",
            "reason": "low_tension_over_reject"
        }

    # ---------- 過早 deep ----------
    if (
        decision["decision"] == "deep"
        and tension < CONFIG["sac"]["min_tension_for_deep"]
    ):
        return {
            "override": True,
            "new_decision": "allow",
            "reason": "low_tension_invalid_deep"
        }

    return {
        "override": False
    }


def apply_sac_override(semantic, decision, plan, state):

    sac = sac_evaluate(semantic, decision, plan, state)

    if not sac.get("override"):
        return decision

    decision["decision"] = sac["new_decision"]
    decision["reason"] = sac["reason"]

    return decision
