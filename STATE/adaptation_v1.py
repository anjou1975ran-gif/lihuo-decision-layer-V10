
---

# 🧠 Feedback-driven Adaptation v1（Production）

---

## I. 目標

```text
根據歷史結果 → 自動調整 decision / profile 行為
```

---

## II. Adaptation Rule

```python
def adapt_strategy(state):

    history = state.get("history", [])

    if len(history) < 3:
        return {}

    recent = history[-3:]

    # ---------- too many rejects ----------
    reject_count = sum(1 for x in recent if x["decision"] == "reject")

    if reject_count >= 2:
        return {
            "adjustment": "loosen_path_threshold"
        }

    # ---------- too many reconstruct ----------
    reconstruct_count = sum(1 for x in recent if x["decision"] == "reconstruct")

    if reconstruct_count >= 2:
        return {
            "adjustment": "increase_direct_answer"
        }

    # ---------- too many holds ----------
    hold_count = sum(1 for x in recent if x["decision"] == "hold")

    if hold_count >= 2:
        return {
            "adjustment": "relax_kairos"
        }

    return {}
```

---

## III. Apply Adaptation

```python
def apply_adaptation(state, decision):

    strategy = adapt_strategy(state)

    if not strategy:
        return decision

    adj = strategy.get("adjustment")

    # ---------- PATH ----------
    if adj == "loosen_path_threshold":
        if decision["decision"] == "reject":
            decision["decision"] = "reconstruct"

    # ---------- RECONSTRUCT ----------
    if adj == "increase_direct_answer":
        if decision["decision"] == "reconstruct":
            decision["decision"] = "allow"

    # ---------- KAIROS ----------
    if adj == "relax_kairos":
        if decision["decision"] == "hold":
            decision["decision"] = "allow"

    return decision
```

---

## IV. Engine Integration（改 decision）

---

### 原本

```python
decision = self.decision(semantic)
```

---

### 👉 改成

```python
decision = self.decision(semantic)
decision = apply_adaptation(self.state, decision)
```

---

## V. Import

```python
from feedback_adaptation_v1 import apply_adaptation
```

---

## VI. Lock

```text
Feedback Adaptation v1 = 自適應決策層（Adaptive Layer）
```

---

