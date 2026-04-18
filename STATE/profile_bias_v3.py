---

# Profile Bias v3（Production）

---

## I. 目標

```text
讓系統開始「偏好某些思考模式」
（不是只調 threshold）
```

---

## II. Bias State

```python
def init_profile_bias():

    return {
        "structural": 0.0,
        "boundary": 0.0,
        "reflective": 0.0
    }
```

---

## III. Extend Adaptive State

```python
def extend_bias_state(state):

    if "adaptive" not in state:
        state = extend_adaptive_state(state)

    if "profile_bias" not in state["adaptive"]:
        state["adaptive"]["profile_bias"] = init_profile_bias()

    return state
```

---

## IV. Update Bias（根據結果調整）

```python
def update_profile_bias(state):

    state = extend_bias_state(state)

    history = state.get("history", [])

    if len(history) < 5:
        return state

    recent = history[-5:]

    bias = state["adaptive"]["profile_bias"]

    for h in recent:

        mode = h.get("mode")

        if mode in bias:

            if h["gate"] == "open":
                bias[mode] += 0.1
            else:
                bias[mode] -= 0.1

    # clamp
    for k in bias:
        bias[k] = max(-1.0, min(1.0, bias[k]))

    return state
```

---

## V. Bias-aware Profile Selection（改 ranking）

👉 改 `select_best_profile`

---

```python
def select_best_profile(semantic, decision, gate_state, state=None):

    best_profile = None
    best_score = -999

    bias = {}
    if state:
        bias = state.get("adaptive", {}).get("profile_bias", {})

    for name, profile in BOUNDARY_PROFILES.items():

        score = score_profile(profile, semantic, gate_state)

        # ---------- 加 bias ----------
        score += bias.get(name, 0.0)

        if score > best_score:
            best_score = score
            best_profile = profile

    if best_score < 1.5:
        return None

    return best_profile
```

---

## VI. Orchestrator Integration

---

### 原本：

```python
profile_obj = select_best_profile(semantic, decision, gate_state)
```

---

### 👉 改成：

```python
profile_obj = select_best_profile(semantic, decision, gate_state, state)
```

---

## VII. Engine Integration

---

### state update 後加：

```python
self.state = update_profile_bias(self.state)
```

---

## VIII. Import

```python
from profile_bias_v3 import update_profile_bias
```

---

## IX. Lock

```text
Profile Bias v3 = 思考偏好層（Preference Layer）
```

---

