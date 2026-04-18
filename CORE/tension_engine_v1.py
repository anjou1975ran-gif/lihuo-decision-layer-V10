def compute_tension(semantic, decision):

    tension = 0.0

    # ---------- 深度 ----------
    if decision["decision"] == "deep":
        tension += 0.5
    elif decision["decision"] == "allow":
        tension += 0.2

    # ---------- 抽象程度 ----------
    if semantic.get("semantic_depth", 0) > 0.7:
        tension += 0.3

    # ---------- 不確定 ----------
    if semantic.get("structure_type") == "incomplete":
        tension += 0.2

    # ---------- 邊界 ----------
    if semantic.get("intent_type") in ["boundary", "philosophy"]:
        tension += 0.4

    # clamp
    return min(tension, 1.0)
