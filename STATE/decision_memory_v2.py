import json
import os
from typing import Dict, Any, List


class DecisionMemoryV2:
    """
    V4 memory layer:
    - store routing outcomes
    - provide hint before decision
    - track deep usefulness by semantic cluster
    """

    def __init__(self, path: str = "repo_root/STATE/decision_memory_v2.json", max_records: int = 500):
        self.path = path
        self.max_records = max_records
        self.data = {
            "records": [],
            "stats": {}
        }
        self._load()

    # -------------------------------------------------
    # IO
    # -------------------------------------------------
    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {"records": [], "stats": {}}

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    # -------------------------------------------------
    # KEYING
    # -------------------------------------------------
    def _semantic_bucket(self, semantic: Dict[str, Any]) -> str:
        intent = semantic.get("intent_type", "unknown")
        structure = semantic.get("structure_type", "unknown")
        depth = float(semantic.get("semantic_depth", 0.0))

        if depth >= 0.85:
            depth_band = "very_high"
        elif depth >= 0.65:
            depth_band = "high"
        elif depth >= 0.4:
            depth_band = "mid"
        else:
            depth_band = "low"

        return f"{intent}|{structure}|{depth_band}"

    # -------------------------------------------------
    # PRE-DECISION HINT
    # -------------------------------------------------
    def get_hint(self, semantic: Dict[str, Any]) -> Dict[str, Any]:
        bucket = self._semantic_bucket(semantic)
        stats = self.data.get("stats", {}).get(bucket)

        if not stats:
            return {
                "hint": "neutral",
                "bucket": bucket,
                "deep_score": 0.0,
                "allow_score": 0.0,
            }

        deep_runs = stats.get("deep_runs", 0)
        deep_success = stats.get("deep_success", 0)
        allow_runs = stats.get("allow_runs", 0)
        allow_success = stats.get("allow_success", 0)

        deep_score = deep_success / deep_runs if deep_runs > 0 else 0.0
        allow_score = allow_success / allow_runs if allow_runs > 0 else 0.0

        hint = "neutral"

        # deep 至少有樣本才准影響
        if deep_runs >= 3 and deep_score >= allow_score + 0.15:
            hint = "prefer_deep"
        elif allow_runs >= 3 and allow_score >= deep_score + 0.15:
            hint = "avoid_deep"

        return {
            "hint": hint,
            "bucket": bucket,
            "deep_score": round(deep_score, 3),
            "allow_score": round(allow_score, 3),
        }

    # -------------------------------------------------
    # POST-EXECUTION UPDATE
    # -------------------------------------------------
    def add_record(
        self,
        semantic: Dict[str, Any],
        decision: Dict[str, Any],
        execution: Dict[str, Any],
        output: Any = None,
    ):
        bucket = self._semantic_bucket(semantic)
        mode = decision.get("mode", "unknown")

        final_confidence = float(execution.get("best_confidence", 0.0))
        iterations = int(execution.get("iterations", 1))
        action_type = execution.get("action_type", execution.get("type", "unknown"))

        # success heuristic
        success = self._judge_success(mode, semantic, execution, output)

        record = {
            "bucket": bucket,
            "intent_type": semantic.get("intent_type"),
            "structure_type": semantic.get("structure_type"),
            "semantic_depth": semantic.get("semantic_depth"),
            "memory_hint_in": semantic.get("memory_hint", "neutral"),
            "mode": mode,
            "action_type": action_type,
            "iterations": iterations,
            "best_confidence": final_confidence,
            "success": success,
        }

        self.data["records"].append(record)
        if len(self.data["records"]) > self.max_records:
            self.data["records"] = self.data["records"][-self.max_records:]

        self._update_stats(bucket, mode, success)
        self._save()

    def _judge_success(
        self,
        mode: str,
        semantic: Dict[str, Any],
        execution: Dict[str, Any],
        output: Any = None,
    ) -> bool:
        intent = semantic.get("intent_type")
        depth = float(semantic.get("semantic_depth", 0.0))
        conf = float(execution.get("best_confidence", 0.0))
        iterations = int(execution.get("iterations", 1))

        if mode == "deep":
            return conf >= 0.7 and iterations >= 1

        if mode == "allow":
            # 淺問題 allow 成功；高深度 allow 視為較弱成功
            if depth < 0.65:
                return True
            return conf >= 0.75

        if mode == "hold":
            return intent in ["boundary", "info", "reasoning", "structure"]

        if mode == "reject":
            return intent == "noise"

        if mode == "reconstruct":
            return True

        return False

    def _update_stats(self, bucket: str, mode: str, success: bool):
        stats = self.data["stats"].setdefault(bucket, {
            "deep_runs": 0,
            "deep_success": 0,
            "allow_runs": 0,
            "allow_success": 0,
            "hold_runs": 0,
            "hold_success": 0,
        })

        if mode == "deep":
            stats["deep_runs"] += 1
            if success:
                stats["deep_success"] += 1

        elif mode == "allow":
            stats["allow_runs"] += 1
            if success:
                stats["allow_success"] += 1

        elif mode == "hold":
            stats["hold_runs"] += 1
            if success:
                stats["hold_success"] += 1

    # -------------------------------------------------
    # DEBUG
    # -------------------------------------------------
    def debug_snapshot(self) -> Dict[str, Any]:
        return {
            "records_count": len(self.data.get("records", [])),
            "stats_keys": list(self.data.get("stats", {}).keys())[:20],
        }
