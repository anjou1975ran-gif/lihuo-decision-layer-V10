import json
import os
from typing import Dict, Any, List


class DecisionMemory:

    def __init__(self, path: str = "repo_root/STATE/memory.json", max_records: int = 200):
        self.path = path
        self.max_records = max_records
        self.data = {"records": []}
        self._load()

    # -------------------------
    # LOAD / SAVE
    # -------------------------
    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except:
                self.data = {"records": []}

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    # -------------------------
    # ADD RECORD
    # -------------------------
    def add_record(self,
                   semantic: Dict[str, Any],
                   decision: Dict[str, Any],
                   execution: Dict[str, Any]):

        record = {
            "intent_type": semantic.get("intent_type"),
            "semantic_depth": semantic.get("semantic_depth"),
            "structure_type": semantic.get("structure_type"),
            "mode": decision.get("mode"),
            "final_confidence": execution.get("best_confidence", 0.0),
            "iterations": execution.get("iterations", 1),
        }

        self.data["records"].append(record)

        # 保留最近 N 筆
        if len(self.data["records"]) > self.max_records:
            self.data["records"] = self.data["records"][-self.max_records:]

        self._save()

    # -------------------------
    # GET HINT（核心）
    # -------------------------
    def get_hint(self, semantic: Dict[str, Any]) -> Dict[str, Any]:

        records = self.data.get("records", [])

        if not records:
            return {"hint": "neutral"}

        intent = semantic.get("intent_type")
        depth = semantic.get("semantic_depth", 0)

        # 篩選類似 case
        similar = [
            r for r in records
            if r["intent_type"] == intent
            and abs(r["semantic_depth"] - depth) < 0.2
        ]

        if len(similar) < 3:
            return {"hint": "neutral"}

        deep_cases = [r for r in similar if r["mode"] == "deep"]
        allow_cases = [r for r in similar if r["mode"] == "allow"]

        def avg_conf(cases: List[Dict]):
            if not cases:
                return 0
            return sum(r["final_confidence"] for r in cases) / len(cases)

        deep_score = avg_conf(deep_cases)
        allow_score = avg_conf(allow_cases)

        # 🔥 判斷
        if deep_score > allow_score + 0.1:
            return {"hint": "prefer_deep"}

        if allow_score > deep_score + 0.1:
            return {"hint": "avoid_deep"}

        return {"hint": "neutral"}
