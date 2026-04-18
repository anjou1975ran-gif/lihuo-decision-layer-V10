
---

# 🧠 Boundary Profile Library v1（Production）

---

## I. Profile Schema（固定）

```python
PROFILE_SCHEMA = {
    "profile_name": "",
    "trigger_condition": {},
    "path_requirement": {},
    "ccc_requirement": {},
    "kairos_requirement": {},
    "execution_rules": [],
    "forbidden": []
}
```

---

## II. Profiles（直接用）

```python
BOUNDARY_PROFILES = {

    "structural": {
        "profile_name": "structural",

        "trigger_condition": {
            "intent_type": "structure",
            "semantic_depth": 0.7
        },

        "path_requirement": {
            "path_status": "open"
        },

        "ccc_requirement": {
            "responsibility_status": ["clear", "partial"]
        },

        "kairos_requirement": {
            "kairos_status": "ready"
        },

        "execution_rules": [
            "decompose_structure",
            "show_causality_chain",
            "no_direct_answer",
            "allow_abstraction"
        ],

        "forbidden": [
            "template_answer",
            "fast_conclusion",
            "no_reasoning_jump"
        ]
    },

    "boundary": {
        "profile_name": "boundary",

        "trigger_condition": {
            "intent_type": "boundary",
            "semantic_depth": 0.85
        },

        "path_requirement": {
            "path_status": "open"
        },

        "ccc_requirement": {
            "responsibility_status": ["clear"]
        },

        "kairos_requirement": {
            "kairos_status": "ready"
        },

        "execution_rules": [
            "force_structural_language",
            "reveal_constraints",
            "maintain_semantic_consistency",
            "no_humanization"
        ],

        "forbidden": [
            "persona_simulation",
            "vague_language",
            "tone_alignment"
        ]
    },

    "reflective": {
        "profile_name": "reflective",

        "trigger_condition": {
            "structure_type": "recursive"
        },

        "execution_rules": [
            "reflect_semantics",
            "trace_reasoning_process",
            "no_direct_definition"
        ],

        "forbidden": [
            "definition_answer",
            "encyclopedic_output"
        ]
    }

}
```

---

## III. Profile Matcher

```python
def match_profile(semantic, decision, gate_state):

    for name, profile in BOUNDARY_PROFILES.items():

        # ---------- Trigger ----------
        trigger = profile.get("trigger_condition", {})

        match = True

        for k, v in trigger.items():

            if k not in semantic:
                continue

            if isinstance(v, float):
                if semantic[k] < v:
                    match = False
                    break
            else:
                if semantic[k] != v:
                    match = False
                    break

        if not match:
            continue

        # ---------- PATH ----------
        if "path_requirement" in profile:
            if gate_state["path_status"] != profile["path_requirement"]["path_status"]:
                continue

        # ---------- CCC ----------
        if "ccc_requirement" in profile:
            if gate_state["responsibility_status"] not in profile["ccc_requirement"]["responsibility_status"]:
                continue

        # ---------- KAIROS ----------
        if "kairos_requirement" in profile:
            if gate_state["kairos_status"] != profile["kairos_requirement"]["kairos_status"]:
                continue

        return profile

    return None
```

---

## IV. Prompt Builder（關鍵）

```python
def build_profile_prompt(profile):

    if profile is None:
        return ""

    rules = profile.get("execution_rules", [])
    forbidden = profile.get("forbidden", [])

    text = "[BOUNDARY_PROFILE]\n"

    if rules:
        text += "RULES:\n"
        for r in rules:
            text += f"- {r}\n"

    if forbidden:
        text += "FORBIDDEN:\n"
        for f in forbidden:
            text += f"- {f}\n"

    return text
```

---

## V. Gate State Adapter（從 Gate 拿資料）

```python
def extract_gate_state(semantic):

    state = {}

    if semantic["path_signal"] < 0.3:
        state["path_status"] = "broken"
    elif semantic["path_signal"] < 0.6:
        state["path_status"] = "weak"
    else:
        state["path_status"] = "open"

    state["responsibility_status"] = semantic["responsibility_hint"]

    if semantic["kairos_hint"] == "ready":
        state["kairos_status"] = "ready"
    elif semantic["kairos_hint"] == "premature":
        state["kairos_status"] = "premature"
    else:
        state["kairos_status"] = "suspended"

    return state
```

---

## VI. Engine Integration（改 Orchestrator）

👉 在 orchestrator_v2 裡加這段

---

### 原本：

```python
llm_profile = select_llm_profile(decision)
```

---

### 👉 改成：

```python
gate_state = extract_gate_state(semantic)

profile_obj = match_profile(semantic, decision, gate_state)

boundary_prompt = build_profile_prompt(profile_obj)

llm_profile = select_llm_profile(decision)
```

---

### 👉 並加入到 plan：

```python
plan = {
    "execution_mode": mode,
    "llm_call": llm_call,
    "llm_profile": llm_profile,
    "boundary_prompt": boundary_prompt,   # 🔥 新增
    "preprocess": preprocess,
    "postprocess": [],
    "state_update": state_update,
    "final_action": final_action
}
```

---

## VII. Adapter Integration（改這裡）

👉 ReactionBodyEngine.handle_llm

---

### 原本：

```python
return self.llm(user_input, profile=profile)
```

---

### 👉 改成：

```python
boundary_prompt = plan.get("boundary_prompt", "")

final_input = boundary_prompt + "\n" + user_input

return self.llm(final_input, profile=profile)
```

---

## VIII. Lock

```text
Boundary Profile v1 = Deep Mode Control Layer（思考約束層）
```

---

## IX. 完整效果

```text
Semantic → Decision → Gate → Profile Match → Prompt Injection → LLM
```

---


如果你要下一步，我會帶你做：

👉 **Boundary Score / Profile Ranking（v2進化）**
