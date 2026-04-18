
---

#Adaptive Profile + Threshold v2（Production）

from CONFIG.config import CONFIG

---

## I. 目標

```text
讓系統不只改 decision
而是「動態調整 Profile / Gate / Threshold」
```

---

## II. Adaptive State Extension

```python
def extend_adaptive_state(state):

    if "adaptive" not in state:
        state["adaptive"] = {
            "path_th = adaptive.get("path_threshold", CONFIG["path_threshold"])": 0.3,
            "deep_th = adaptive.get("deep_threshold", CONFIG["deep_threshold"])": 0.8,
            "kairos_relax": False,
            "profile_bias": {}
        }

    return state
```

---

## III. Adaptive Analyzer

```python
def analyze_adaptation(state):

    history = state.get("history", [])

    if len(history) < 5:
        return None

    recent = history[-5:]

    stats = {
        "reject": 0,
        "reconstruct": 0,
        "hold": 0,
        "deep": 0
    }

    for h in recent:
        stats[h["decision"]] = stats.get(h["decision"], 0) + 1

    return stats
```

---

## IV. Adaptive Update

```python
def update_adaptive_rules(state):

    state = extend_adaptive_state(state)

    stats = analyze_adaptation(state)

    if not stats:
        return state

    adaptive = state["adaptive"]

    # ---------- PATH ----------
    if stats["reject"] >= 3:
        adaptive["path_threshold"] = max(0.1, adaptive["path_threshold"] - 0.05)

    # ---------- RECONSTRUCT ----------
    if stats["reconstruct"] >= 3:
        adaptive["deep_threshold"] = max(0.6, adaptive["deep_threshold"] - 0.05)

    # ---------- HOLD ----------
    if stats["hold"] >= 3:
        adaptive["kairos_relax"] = True

    # ---------- DEEP ----------
    if stats["deep"] >= 3:
        adaptive["deep_threshold"] = min(0.95, adaptive["deep_threshold"] + 0.05)

    return state
```

---

## V. Adaptive Decision Hook

```python
def apply_adaptive_thresholds(state, semantic, decision):

    adaptive = state.get("adaptive", {})

    path_th = adaptive.get("path_threshold", 0.3)
    deep_th = adaptive.get("deep_threshold", 0.8)

    # ---------- PATH ----------
    if semantic["path_signal"] < path_th:
        decision["decision"] = "reject"

    # ---------- DEEP ----------
    if semantic["semantic_depth"] > deep_th:
        if decision["decision"] == "allow":
            decision["decision"] = "deep"

    # ---------- KAIROS ----------
    if adaptive.get("kairos_relax", False):
        if decision["decision"] == "hold":
            decision["decision"] = "allow"

    return decision
```

---

## VI. Engine Integration（兩處）

---

### 1️⃣ decision 後

```python
decision = self.decision(semantic)
decision = apply_adaptation(self.state, decision)
decision = apply_adaptive_thresholds(self.state, semantic, decision)
```

---

### 2️⃣ state update 後

```python
self.state = update_engine_state(...)
self.state = update_adaptive_rules(self.state)
```

---

## VII. Import

```python
from adaptive_profile_threshold_v2 import (
    apply_adaptive_thresholds,
    update_adaptive_rules
)
```

---

## VIII. Lock

```text
Adaptive Profile v2 = 動態策略層（Dynamic Control Layer）
```

---

