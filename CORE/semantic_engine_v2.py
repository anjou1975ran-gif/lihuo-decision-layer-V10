import re

def semantic_engine_v2(user_input: str):

    text = user_input.strip()
    length = len(text)

    has_question = "?" in text or "？" in text

    # 🔥 擴充關鍵詞（核心修復）
    has_tool_words = any(k in text for k in [
        "寫", "幫我", "給我", "翻譯",
        "輸出", "列出", "生成", "整理", "用清單"
    ])

    has_boundary_words = any(k in text for k in [
        "邊界", "限制",
        "是否應該", "判斷條件", "不下結論", "只能", 
        "在什麼條件下" 
    ])

    has_structure_words = any(k in text for k in [
        "結構", "本質", "原理", "怎麼運作", "模組"
    ])

    
    has_meta_words = any(k in text for k in [
        "語義空間", "自我引用", "理解", "記憶",
        "表徵", "表示", "語言模型", "embedding",
        "認知", "推理過程"
    ])

    has_reflection = any(k in text for k in [
        "如何形成", "為什麼會", "本質是什麼",
        "如何理解", "怎麼理解", "如何運作"
    ])

    has_why = any(k in text for k in ["為什麼", "why"])
    has_how = any(k in text for k in ["怎麼", "如何"])
    has_what = any(k in text for k in ["是什麼", "什麼是"])
    
    # ---------------- NOISE ----------------
    is_noise_pattern = (
        (length <= 4 and not has_question)
        or re.fullmatch(r"[a-zA-Z]+", text)
        or re.fullmatch(r"\d+", text)
    )

    is_noise = (
        is_noise_pattern
        and not has_why
        and not has_how
        and not has_what
    )

    # ---------------- INTENT ----------------
    if is_noise:
        intent_type = "noise"
    elif has_boundary_words:
        intent_type = "boundary"
    elif has_tool_words:
        intent_type = "tool"
    elif has_structure_words:
        intent_type = "structure"
    elif has_why or has_how:
        intent_type = "reasoning"
    else:
        intent_type = "info"

    # ---------------- DEPTH ----------------
    semantic_depth = 0.0

    if has_meta_words:
        semantic_depth += 0.3
    if has_what:
        semantic_depth += 0.2
    if has_why:
        semantic_depth += 0.35
    if has_how:
        semantic_depth += 0.35

    if has_structure_words:
        semantic_depth += 0.5

    if has_boundary_words:
        semantic_depth += 0.45

    # 🔥 新增
    if has_reflection:
        semantic_depth += 0.35

    # 🔥 關鍵補強（你原本太弱）
    if has_question and length > 20:
        semantic_depth += 0.2

    # 🔥 保留但降低權重（避免灌水）
    elif length > 20:
        semantic_depth += 0.1

    semantic_depth = min(1.0, semantic_depth)

    # ---------------- STRUCTURE ----------------
    if intent_type == "noise":
        structure_type = "none"
    elif intent_type == "tool":
        structure_type = "complete"
    elif intent_type == "boundary":
        structure_type = "recursive"
    elif not has_question and semantic_depth < 0.4:
        structure_type = "incomplete"
    else:
        structure_type = "complete"

    # ---------------- COHERENCE ----------------
    if intent_type == "noise":
        coherence = 0.1
    elif structure_type == "incomplete":
        coherence = 0.5
    else:
        coherence = 0.6 + (semantic_depth * 0.3)

    signal_strength = semantic_depth * 0.6 + coherence * 0.4

    risk_flags = []
    if structure_type == "incomplete":
        risk_flags.append("undefined_scope")

    # ---------------- PATH ----------------
    path_signal = 0.4 + semantic_depth * 0.4

    if coherence < 0.4:
        path_signal -= 0.3
    if structure_type == "none":
        path_signal -= 0.4
    if "undefined_scope" in risk_flags:
        path_signal -= 0.1
    if intent_type in ["structure", "boundary"]:
        path_signal += 0.3

    path_signal = max(0.0, min(1.0, path_signal))

    # ---------------- RESPONSIBILITY ----------------
    if intent_type == "tool":
        responsibility_hint = "clear"
    elif structure_type == "incomplete":
        responsibility_hint = "partial"
    else:
        responsibility_hint = "clear"

    # ---------------- KAIROS ----------------
    if semantic_depth > 0.7 and coherence > 0.7:
        kairos_hint = "ready"
    elif structure_type == "incomplete" and semantic_depth < 0.4:
        kairos_hint = "premature"
    else:
        kairos_hint = "weak"

    # ---------------- MODE ----------------
    if intent_type == "noise":
        mode_hint = "reject"
    elif semantic_depth > 0.6 and kairos_hint in ["ready", "weak"]:
        mode_hint = "deep"
    elif structure_type == "incomplete":
        mode_hint = "reconstruct"
    else:
        mode_hint = "allow"

    return {
        "intent_type": intent_type,
        "semantic_depth": round(semantic_depth, 2),
        "structure_type": structure_type,
        "coherence": round(coherence, 2),
        "signal_strength": round(signal_strength, 2),
        "path_signal": round(path_signal, 2),
        "responsibility_hint": responsibility_hint,
        "kairos_hint": kairos_hint,
        "risk_flags": risk_flags,
        "mode_hint": mode_hint,
    }
