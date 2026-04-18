"""Decision core v2."""

from typing import Dict, List, Any


# ===== HARD LOCK（第一階段穩定器） =====

def hard_lock_mode(semantic: Dict[str, Any]) -> str:
    intent = semantic.get("intent_type", "")

    if intent == "noise":
        return "reject"
    elif intent == "tool":
        return "allow"
    elif intent in ["structure", "reasoning"]:
        # 這只是初始傾向，不是最終裁決
        return "deep"
    elif intent == "boundary":
        return "hold"
    else:
        # info / unknown 預設不要太保守，先給 allow 傾向
        return "allow"


def generate_candidates(_: Dict[str, Any]) -> List[Dict[str, str]]:
    return [
        {"mode": "reject"},
        {"mode": "reconstruct"},
        {"mode": "allow"},
        {"mode": "deep"},
        {"mode": "hold"},
    ]


# ===== KERNELS =====

def sac_kernel(s: Dict[str, Any]) -> Dict[str, Any]:
    tension = 0.0

    if s.get("intent_type") in ["structure", "boundary"]:
        tension += 0.4

    if s.get("structure_type") == "recursive":
        tension += 0.3

    if "contradiction" in s.get("risk_flags", []):
        tension += 0.2

    return {
        "tension_level": min(1.0, tension),
        "tension_type": (
            "boundary"
            if s.get("intent_type") == "boundary"
            else "structural" if s.get("intent_type") == "structure"
            else "none"
        ),
    }


def ccc_kernel(s: Dict[str, Any]) -> Dict[str, Any]:
    return {"responsibility_status": s.get("responsibility_hint", "unknown")}


def path_kernel(s: Dict[str, Any]) -> Dict[str, Any]:
    signal = float(s.get("path_signal", 0.0))

    if signal < 0.3:
        status = "broken"
    elif signal < 0.6:
        status = "weak"
    else:
        status = "open"

    return {"path_status": status}


def kairos_kernel(s: Dict[str, Any]) -> Dict[str, Any]:
    hint = s.get("kairos_hint")

    if hint == "ready":
        return {"kairos_status": "ready"}
    elif hint == "premature":
        return {"kairos_status": "premature"}
    elif hint == "weak":
        return {"kairos_status": "weak"}
    else:
        return {"kairos_status": "suspended"}


# ===== EVALUATION =====

def evaluate_candidate(c: Dict[str, str], semantic: Dict[str, Any], kernels: Dict[str, Any]) -> str:
    sac = kernels["sac"]
    ccc = kernels["ccc"]
    path = kernels["path"]
    kairos = kernels["kairos"]

    mode = c["mode"]
    base_mode = hard_lock_mode(semantic)
    intent = semantic.get("intent_type")
    structure_type = semantic.get("structure_type")

    # =========================================
    # HARD REJECT / HARD BLOCK
    # =========================================
    if intent == "noise":
        return "feasible" if mode == "reject" else "invalid"

    if path["path_status"] == "broken":
        # 路徑斷裂時，禁止 allow / deep
        if mode == "reject":
            return "feasible"
        if mode in ["reconstruct", "hold"]:
            return "unstable"
        return "invalid"

    # =========================================
    # TOOL（高優先）
    # =========================================
    if intent == "tool":
        if mode == "allow":
            return "feasible"
        if mode == "reconstruct":
            return "unstable"
        return "invalid"

    # =========================================
    # RESPONSIBILITY
    # =========================================
    if ccc["responsibility_status"] == "missing":
        if mode == "reconstruct":
            return "feasible"
        if mode == "hold":
            return "feasible"
        return "invalid"

    # =========================================
    # INCOMPLETE
    # =========================================
    if structure_type == "incomplete":
        if mode == "reconstruct":
            return "feasible"


        if mode == "hold":
            return "feasible"

        return "invalid"

    # ================================
    # HIGH TENSION / DEEP ROUTING
    # ================================

    if intent in ["structure", "boundary", "reasoning"]:

        # 🔥 boundary 特殊處理
        if intent == "boundary":
            if mode == "hold":
                return "feasible"
            if mode == "deep":
                return "unstable"
            return "invalid"

        # 🔥 deep 判斷（主路徑）
        if (
            sac["tension_level"] > 0.45
            or semantic.get("semantic_depth", 0) > 0.65
            or semantic.get("memory_hint") == "prefer_deep"
        ):
            if mode == "deep":
                return "feasible"
            if mode == "allow":
                return "unstable"
            return "invalid"

    # =========================================
    # KAIROS CONTROL
    # =========================================
    if kairos["kairos_status"] in ["premature", "suspended"]:
        if intent in ["reasoning", "structure"]:
            if mode == "hold":
                return "feasible"
            if mode == "reconstruct":
                return "unstable"
            return "invalid"

    # =========================================
    # WEAK PATH
    # =========================================
    if path["path_status"] == "weak":
        if mode == "hold":
            return "feasible"

        # 關鍵放寬：
        # tool / info 在弱路徑下仍可保留 allow 候選
        if mode == "allow" and intent in ["tool", "info"]:
            return "feasible"

        return "invalid"

    # =========================================
    # STRUCTURE / REASONING
    # =========================================
    if intent in ["structure", "reasoning"]:
        if kairos["kairos_status"] == "ready":
            if mode == "deep":
                return "feasible"
            if mode == "allow":
                return "unstable"
            return "invalid"

        if kairos["kairos_status"] == "weak":
            if mode == "allow":
                return "feasible"
            if mode == "deep":
                return "unstable"
            if mode == "hold":
                return "unstable"
            return "invalid"

        return "feasible" if mode == "hold" else "invalid"

    # =========================================
    # BOUNDARY
    # =========================================
    if intent == "boundary":
        if mode == "hold":
            return "feasible"
        if mode == "allow":
            return "invalid"   # 🔥 明確禁止
        return "invalid"

    # =========================================
    # INFO
    # =========================================
    # 給 semantic 誤判過保守時一個出口
    if intent == "info":
        if mode == "allow":
            return "feasible"
        if mode == "reconstruct":
            return "unstable"
        return "invalid"

    # =========================================
    # DEFAULT = hard lock as fallback
    # =========================================
    return "feasible" if mode == base_mode else "invalid"

    def select_mode(
        feasible: List[Dict[str, str]],
        unresolved: List[Dict[str, str]],
        semantic: Dict[str, Any],
        kernels: Dict[str, Any],
        ) -> str:
        
        feasible_modes = [c["mode"] for c in feasible]
        unresolved_modes = [c["mode"] for c in unresolved]

    # 🔥 MEMORY 控制（放這裡！）
    if semantic.get("memory_hint") == "avoid_deep":
        if "deep" in feasible_modes:
            feasible_modes.remove("deep")

    # 明確優先序：
    # reject > allow > deep > hold > reconstruct
    if "reject" in feasible_modes:
        return "reject"

    # 🔥 關鍵：只在「高張力」時優先 deep
    if "deep" in feasible_modes:
        if (
            kernels["sac"]["tension_level"] > 0.6
            or semantic.get("memory_hint") == "prefer_deep"
        ):
            return "deep"

    if "allow" in feasible_modes:
        return "allow"

    if "hold" in feasible_modes:
        return "hold"

    if "reconstruct" in feasible_modes:
        return "reconstruct"

    # 沒有 feasible 時，才看 unresolved
    if "allow" in unresolved_modes:
        return "allow"

    if "deep" in unresolved_modes:
        return "deep"

    if "hold" in unresolved_modes:
        return "hold"

    if "reconstruct" in unresolved_modes:
        return "reconstruct"

    return hard_lock_mode(semantic)


    # ===== CORE =====

    def decision_core_v2(semantic: Dict[str, Any]) -> Dict[str, Any]:
        sac = sac_kernel(semantic)
        ccc = ccc_kernel(semantic)
        path = path_kernel(semantic)
        kairos = kairos_kernel(semantic)

        kernels = {
            "sac": sac,
            "ccc": ccc,
            "path": path,
            "kairos": kairos,
        }

        candidates = generate_candidates(semantic)

        feasible = []
        rejected = []
        unresolved = []

    for c in candidates:
        status = evaluate_candidate(c, semantic, kernels)

        if status == "invalid":
            rejected.append(c)
        elif status == "unstable":
            unresolved.append(c)
        else:
            feasible.append(c)

    mode = select_mode(feasible, unresolved, semantic, kernels)

    return {
        "mode": mode,
        "state_space": {
            "feasible": feasible,
            "rejected": rejected,
            "unresolved": unresolved,
        },
        "kernels": kernels,
    }
