"""
Decision Core v3 — FULL STRUCTURE VERSION

Integrated:
- PATH (feasibility)
- KAIROS (timing)
- SAC (tension)
- CCC (responsibility)

Goal:
Stop fake reasoning.
Stop forced completion.
Preserve structural integrity.
"""

from typing import Dict, List, Any


# =========================================================
# HARD LOCK（第一層：快速穩定器）
# =========================================================

def hard_lock_mode(semantic: Dict[str, Any]) -> str:
    intent = semantic.get("intent_type", "")

    if intent == "noise":
        return "reject"

    elif intent == "tool":
        return "allow"

    elif intent in ["structure", "reasoning"]:
        return "deep"

    elif intent == "boundary":
        return "hold"

    return "allow"


# =========================================================
# CANDIDATES
# =========================================================

def generate_candidates(_: Dict[str, Any]) -> List[Dict[str, str]]:
    return [
        {"mode": "reject"},
        {"mode": "reconstruct"},
        {"mode": "allow"},
        {"mode": "deep"},
        {"mode": "hold"},
    ]


# =========================================================
# KERNELS
# =========================================================

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
    return {
        "responsibility_status": s.get("responsibility_hint", "unknown")
    }


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


# =========================================================
# EVALUATION CORE（🔥核心修正區）
# =========================================================

def evaluate_candidate(
    c: Dict[str, str],
    semantic: Dict[str, Any],
    kernels: Dict[str, Any]
) -> str:

    sac = kernels["sac"]
    ccc = kernels["ccc"]
    path = kernels["path"]
    kairos = kernels["kairos"]

    mode = c["mode"]
    intent = semantic.get("intent_type")
    structure_type = semantic.get("structure_type")

    # =====================================================
    # ❌ PATH 斷裂 → 直接封鎖（關鍵修正）
    # =====================================================
    if path["path_status"] == "broken":
        if mode == "reject":
            return "feasible"
        if mode in ["reconstruct", "hold"]:
            return "unstable"
        return "invalid"

    # =====================================================
    # ❌ NOISE
    # =====================================================
    if intent == "noise":
        return "feasible" if mode == "reject" else "invalid"

    # =====================================================
    # 🛠 TOOL（優先權高）
    # =====================================================
    if intent == "tool":
        if mode == "allow":
            return "feasible"
        if mode == "reconstruct":
            return "unstable"
        return "invalid"

    # =====================================================
    # ⚖️ CCC（責任缺失）
    # =====================================================
    if ccc["responsibility_status"] == "missing":
        if mode in ["reconstruct", "hold"]:
            return "feasible"
        return "invalid"

    # =====================================================
    # 🧩 結構未完成
    # =====================================================
    if structure_type == "incomplete":
        if mode in ["reconstruct", "hold"]:
            return "feasible"
        return "invalid"

    # =====================================================
    # 🔥 SAC（高張力 → 深推理）
    # =====================================================
    if intent in ["structure", "reasoning"]:

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

    # =====================================================
    # 🧭 BOUNDARY（🔥你之前壞掉的地方）
    # =====================================================
    if intent == "boundary":
        if mode == "hold":
            return "feasible"
        if mode == "deep":
            return "unstable"
        return "invalid"

    # =====================================================
    # ⏳ KAIROS（時機控制）
    # =====================================================
    if kairos["kairos_status"] in ["premature", "suspended"]:
        if mode == "hold":
            return "feasible"
        if mode == "reconstruct":
            return "unstable"
        return "invalid"

    # =====================================================
    # ⚠️ WEAK PATH（弱路徑）
    # =====================================================
    if path["path_status"] == "weak":
        if mode == "hold":
            return "feasible"
        if intent in ["tool", "info"] and mode == "allow":
            return "unstable"
        return "invalid"

    # =====================================================
    # ✅ DEFAULT（穩定狀態）
    # =====================================================
    if mode == "allow":
        return "feasible"

    if mode == "reconstruct":
        return "unstable"

    return "invalid"

def select_mode(
    feasible: List[Dict[str, str]],
    unresolved: List[Dict[str, str]],
    semantic: Dict[str, Any],
    kernels: Dict[str, Any],
) -> str:
    feasible_modes = [c["mode"] for c in feasible]
    unresolved_modes = [c["mode"] for c in unresolved]

    sac = kernels["sac"]
    path = kernels["path"]
    kairos = kernels["kairos"]

    intent = semantic.get("intent_type")
    depth = float(semantic.get("semantic_depth", 0.0))
    memory_hint = semantic.get("memory_hint", "neutral")

    # -------------------------------------------------
    # 強制優先：reject
    # -------------------------------------------------
    if "reject" in feasible_modes:
        return "reject"

    # -------------------------------------------------
    # boundary 一律 hold 優先
    # -------------------------------------------------
    if intent == "boundary" and "hold" in feasible_modes:
        return "hold"

    # -------------------------------------------------
    # avoid_deep 只壓低深度問題，不壓高深度
    # -------------------------------------------------
    if memory_hint == "avoid_deep" and depth < 0.85:
        if "deep" in feasible_modes:
            feasible_modes.remove("deep")

    # -------------------------------------------------
    # 高深度 / memory / 高張力 → deep
    # -------------------------------------------------
    if "deep" in feasible_modes:
        if (
            sac["tension_level"] > 0.45
            or depth > 0.65
            or memory_hint == "prefer_deep"
            or (depth >= 0.85 and intent in ["structure", "reasoning"])
        ):
            return "deep"

    # -------------------------------------------------
    # premature / suspended → hold
    # -------------------------------------------------
    if kairos["kairos_status"] in ["premature", "suspended"]:
        if "hold" in feasible_modes:
            return "hold"

    # -------------------------------------------------
    # weak path → hold 優先
    # -------------------------------------------------
    if path["path_status"] == "weak":
        if "hold" in feasible_modes:
            return "hold"

    # -------------------------------------------------
    # 一般 allow
    # -------------------------------------------------
    if "allow" in feasible_modes:
        return "allow"

    # -------------------------------------------------
    # reconstruct
    # -------------------------------------------------
    if "reconstruct" in feasible_modes:
        return "reconstruct"

    # -------------------------------------------------
    # unresolved fallback
    # -------------------------------------------------
    if "hold" in unresolved_modes:
        return "hold"

    return "reject"


def decision_core_v3(semantic: Dict[str, Any]) -> Dict[str, Any]:
    kernels = {
        "sac": sac_kernel(semantic),
        "ccc": ccc_kernel(semantic),
        "path": path_kernel(semantic),
        "kairos": kairos_kernel(semantic),
    }

    candidates = generate_candidates(semantic)

    feasible: List[Dict[str, str]] = []
    rejected: List[Dict[str, str]] = []
    unresolved: List[Dict[str, str]] = []

    for candidate in candidates:
        status = evaluate_candidate(candidate, semantic, kernels)
        if status == "invalid":
            rejected.append(candidate)
        elif status == "unstable":
            unresolved.append(candidate)
        else:
            feasible.append(candidate)

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
