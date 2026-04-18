

---

# 🧠 Boundary Score v2（Production）


from CONFIG.config import CONFIG

---

## I. Goal

```text
多 Profile 競爭 → 選最佳（不是第一個 match）
```

---

## II. Score Function

```python
def score_profile(profile, semantic, gate_state):

    score = 0.0

    trigger = profile.get("trigger_condition", {})

    for k, v in trigger.items():

        if k not in semantic:
            continue

        if isinstance(v, float):
            score += min(1.0, semantic[k] / v)
        else:
            if semantic[k] == v:
                score += 1.0

    # PATH
    if "path_requirement" in profile:
        if gate_state["path_status"] == profile["path_requirement"]["path_status"]:
            score += 1.0

    # CCC
    if "ccc_requirement" in profile:
        if gate_state["responsibility_status"] in profile["ccc_requirement"]["responsibility_status"]:
            score += 1.0

    # KAIROS
    if "kairos_requirement" in profile:
        if gate_state["kairos_status"] == profile["kairos_requirement"]["kairos_status"]:
            score += 1.0

    return score
```

---

## III. Ranking Selector

```python
def select_best_profile(semantic, decision, gate_state):

    best_profile = None
    best_score = 0.0

    for name, profile in BOUNDARY_PROFILES.items():

        score = score_profile(profile, semantic, gate_state)

        if score > best_score:
            best_score = score
            best_profile = profile

    # 最低門檻（防亂觸發）
    if best_score < CONFIG["profile"]["score_threshold"]:
        return None

    return best_profile
```

---

## IV. Replace Matcher（關鍵改這裡）

---

### ❌ 舊：

```python
profile_obj = match_profile(semantic, decision, gate_state)
```

---

### ✅ 新：

```python
profile_obj = select_best_profile(semantic, decision, gate_state)
```

---

## V. Debug（可選）

```python
def debug_profile_scores(semantic, gate_state):

    for name, profile in BOUNDARY_PROFILES.items():
        s = score_profile(profile, semantic, gate_state)
        print(f"{name}: {round(s,2)}")
```

---

## VI. Lock

```text
Boundary Score v2 = Profile Selection Authority
```

---

