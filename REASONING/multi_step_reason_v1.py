

---

# Multi-Step Reason Control v1（Production）

---

## I. 目標

```text id="2l6s0e"
讓回應變成「多階段推理流程」
而不是一次輸出
```

---

## II. Reason Plan Schema

```python id="5x5t6l"
REASON_PLAN = {
    "steps": [],
    "current_step": 0,
    "completed": False
}
```

---

## III. Build Reason Plan

```python id="yzif2d"
def build_reason_plan(execution_plan):

    mode = execution_plan.get("mode", "normal")

    # ---------- STRUCTURAL ----------
    if mode == "structural":
        return {
            "steps": [
                "identify_components",
                "map_relations",
                "derive_causality",
                "finalize_structure"
            ],
            "current_step": 0,
            "completed": False
        }

    # ---------- BOUNDARY ----------
    if mode == "boundary":
        return {
            "steps": [
                "define_boundary",
                "expose_constraints",
                "stabilize_system"
            ],
            "current_step": 0,
            "completed": False
        }

    # ---------- REFLECTIVE ----------
    if mode == "reflective":
        return {
            "steps": [
                "trace_origin",
                "inspect_reasoning",
                "reconstruct_meaning"
            ],
            "current_step": 0,
            "completed": False
        }

    # ---------- DEFAULT ----------
    return {
        "steps": ["direct_answer"],
        "current_step": 0,
        "completed": False
    }
```

---

## IV. Step Controller

```python id="7dx0kp"
def get_current_step(reason_plan):

    steps = reason_plan["steps"]
    idx = reason_plan["current_step"]

    if idx >= len(steps):
        return None

    return steps[idx]
```

---

## V. Step Progression

```python id="6c4jhf"
def advance_reason_plan(reason_plan):

    reason_plan["current_step"] += 1

    if reason_plan["current_step"] >= len(reason_plan["steps"]):
        reason_plan["completed"] = True

    return reason_plan
```

---

## VI. Step Injection（關鍵）

```python id="x9hv1g"
def inject_reason_step(user_input, reason_plan):

    step = get_current_step(reason_plan)

    if step is None:
        return user_input

    return f"[REASON_STEP: {step}]\n{user_input}"
```

---

## VII. Orchestrator Integration

---

### 新增 import

```python id="ch4n8n"
from multi_step_reason_v1 import build_reason_plan
```

---

### 在 execution_plan 後加：

```python id="y5c9r0"
reason_plan = build_reason_plan(execution_plan)
```

---

### 加進 plan：

```python id="0mxx6n"
"reason_plan": reason_plan,
```

---

## VIII. Engine Integration（改 handle_llm）

---

### 新增 import

```python id="v8jq3n"
from multi_step_reason_v1 import inject_reason_step, advance_reason_plan
```

---

### 修改 handle_llm

```python id="9n8i2q"
def handle_llm(self, user_input, plan):

    profile = plan.get("llm_profile", "surface")
    boundary_prompt = plan.get("boundary_prompt", "")
    execution_plan = plan.get("execution_plan", {})
    reason_plan = self.state.get("reason_plan", plan.get("reason_plan", {}))

    stepped_input = inject_reason_step(user_input, reason_plan)

    controlled_input = apply_execution_control(stepped_input, execution_plan)

    final_input = boundary_prompt + "\n" + controlled_input

    if self.llm is None:
        output = f"[LLM_CALL:{profile}]\n{final_input}"
    else:
        output = self.llm(final_input, profile=profile)

    advance_reason_plan(reason_plan)

    self.state["reason_plan"] = reason_plan

    return output
```

---

## IX. Lock

```text id="q1w2er"
Multi-Step Reason v1 = 分段推理控制層（Stepwise Reasoning Layer）
```

---

