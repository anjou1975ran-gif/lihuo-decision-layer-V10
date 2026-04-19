print("🔥 USING FILE:", __file__)
import CORE.branch_policy_layer as bpl
print("USING POLICY FILE:", bpl.__file__)
from CONFIG.config import CONFIG
from CORE.branch_policy_layer import BRANCH_POLICIES
from CORE.semantic_engine_v2 import semantic_engine_v2
from CORE.decision_core_v3 import decision_core_v3
from CORE.orchestrator_v2 import orchestrator_v2
from CORE.gate_runtime_v2 import gate_runtime_v2
from EXECUTION.execution_layer_v1 import apply_execution_control
from EXECUTION.execution_layer_v1 import execution_layer_v1
from EXECUTION.deep_execution_v4 import deep_execute
from STATE.memory_feedback_v1 import (
    init_engine_state,
    update_engine_state,
    resolve_pending,
    build_feedback_record
)

from STATE.trace_system_v1 import build_trace
from STATE.decision_memory_v2 import DecisionMemoryV2
from CORE.cost_control_v1 import cost_control_v1
from CORE.failure_detector_v1 import failure_detector_v1


def build_branch_prompt(input_text: str, path: str):
    if path == "causal":
        return (
            "你現在走的是【因果推理路徑】。\n"
            "請回答這個問題時，優先分析：原因、形成機制、導致的結果。\n"
            "避免只下定義，要說明它是怎麼形成的。\n\n"
            f"問題：{input_text}"
        )

    if path == "structural":
        return (
            "你現在走的是【結構推理路徑】。\n"
            "請回答這個問題時，優先分析：組成關係、層級、內部結構、是否存在遞迴或自我引用。\n"
            "避免只講表面意思，要指出內部是怎麼被組成的。\n\n"
            f"問題：{input_text}"
        )

    if path == "systemic":
        return (
            "你現在走的是【系統推理路徑】。\n"
            "請回答這個問題時，優先分析：如果它是一個系統、模型或流程，它如何運作、如何輸出結果、有哪些限制。\n"
            "避免只談概念，要說明它作為系統時怎麼跑。\n\n"
            f"問題：{input_text}"
        )

    return f"問題：{input_text}"

def generate_branches(input_text: str, semantic: dict):
    """
    V7.5: 分支不只是一個標籤，而是各自有 prompt
    """

    intent = semantic.get("intent_type", "")
    depth = semantic.get("semantic_depth", 0.0)

    paths = ["causal", "structural", "systemic"]

    if intent == "boundary" and depth < 0.6:
        paths = ["systemic"]

    branches = []
    for path in paths:
        branches.append({
            "path": path,
            "policy": BRANCH_POLICIES.get(path, {}),   # 🔥 加這行
            "prompt": build_branch_prompt(input_text, path),
            "reasoning": f"[{path}] branch prepared",
            "answer": None,
        })

    return branches

def evaluate_branch(branch: dict, semantic: dict):
    intent = semantic.get("intent_type", "")
    depth = float(semantic.get("semantic_depth", 0.0))
    structure_type = semantic.get("structure_type", "")

    path = branch["path"]
    answer = branch.get("answer", "")
    score = 0.0

    if path == "causal":
        if intent == "reasoning":
            score += 0.4
        if depth >= 0.7:
            score += 0.2
        if "原因" in answer or "機制" in answer:
            score += 0.1

    elif path == "structural":
        if intent in ["structure", "reasoning"]:
            score += 0.35
        if structure_type in ["complete", "recursive"]:
            score += 0.25
        if "結構" in answer or "組成" in answer:
            score += 0.15

    elif path == "systemic":
        if intent in ["tool", "reasoning", "structure"]:
            score += 0.25
        if depth >= 0.6:
            score += 0.15
        if "系統" in answer or "流程" in answer:
            score += 0.1

    return round(score, 3)

def evaluate_branch_with_policy(branch, semantic):
    policy = branch.get("policy", {})
    answer = branch.get("answer", "")

    base_score = evaluate_branch(branch, semantic)

    bonus = 0.0
    penalty = 0.0

    for rule in policy.get("valid_claim", []):
        if rule in answer:
            bonus += 0.2

    for rule in policy.get("fatal_error", []):
        if rule in answer:
            penalty += 0.3

    return round(base_score + bonus - penalty, 3)


def check_branch_fatal(branch, semantic):
    """
    🔥 V9：判斷這條 branch 是否應該直接死亡
    """

    policy = branch.get("policy", {})
    answer = branch.get("answer", "")

    fatal_rules = policy.get("fatal_error", [])

    # 🔥 最簡版：關鍵字觸發（你之後可以升級）
    for rule in fatal_rules:
        if rule in answer:
            return {
                "is_fatal": True,
                "reason": rule
            }

    return {
        "is_fatal": False,
        "reason": None
    }

def check_branch_stop(branch, semantic):
    """
    🔥 V9.5：判斷這條 branch 是否應該停止（不是死亡）
    """

    policy = branch.get("policy", {})
    answer = branch.get("answer", "")

    stop_rules = policy.get("stop_condition", [])

    for rule in stop_rules:
        if rule in answer:
            return {
                "is_stop": True,
                "reason": rule
            }

    return {
        "is_stop": False,
        "reason": None
    }


def select_best_branch(branches: list, semantic: dict):
    scored = []

    for b in branches:
        score = evaluate_branch(b, semantic)
        item = {
            "path": b["path"],
            "reasoning": b["reasoning"],
            "answer": b["answer"],
            "score": score,
        }
        scored.append(item)

    best = max(scored, key=lambda x: x["score"])

    return {
        "best": best,
        "all": scored
    }

def normalize_structural_signal(input_text: str) -> dict:
    text = input_text.lower().strip()

    triggers = {
        "causal_break": [
            "reasoning is wrong",
            "reasoning path has flaws",
            "flawed reasoning",
            "broken causal chain",
            "causal chain is incomplete",
            "missing steps",
            "hidden assumptions",
            "wrong method",
            "partially incorrect",
            "not structurally verified",
            "reasoning is flawed",
            "incorrect reasoning",
            "flawed method",
        ],
        "outcome_justifies_error": [
            "result is correct",
            "outcome is correct",
            "beneficial results",
            "good outcomes",
            "correct answer",
            "expected result",
            "improves efficiency",
            "produces correct answers",
            "final answer is correct",
            "final answer happens to be correct",
            "beneficial results",
        ],
        "responsibility_missing": [
            "responsibility cannot be traced",
            "responsibility is unclear",
            "cannot be assigned",
            "cannot be clearly assigned",
            "responsibility for the decision cannot be traced",
        ],
        "insufficient_context": [
            "not enough information",
            "conditions are incomplete",
            "evidence is incomplete",
            "necessary conditions are missing",
            "not fully verified",
        ],
        "unresolved_multipath": [
            "multiple solutions exist",
            "multiple interpretations remain",
            "two reasoning paths exist",
            "both plausible but unresolved",
            "no clear evaluation criteria",
        ],
        "premature_decision": [
            "decision is required immediately",
            "should the system proceed",
            "should the system still give a final answer",
            "should the system generate a decision",
            "force a conclusion",
            "force a final answer",
        ],
        "structurally_valid": [
            "all constraints are complete",
            "reasoning is valid",
            "causality is verified",
            "data is complete",
            "no structural conflict exists",
            "responsibility is clear",
            "all conditions are satisfied",
            "logic is internally consistent",
        ],
        "implicit_violation": [
            "contains errors",
            "violates structural rules",
            "not structurally verified",
            "cannot be verified",
            "appears reasonable",
            "seems reasonable",
            "persuasive",
            "coherent but",
            "error exists",
            "will never be discovered",
            "should it be acceptable",
            "produces correct answers",
            "responsibility for the decision cannot be traced",
            "users prefer confident output",
            "justify flawed reasoning using correct outcomes",
        ],
        "uncertainty_hiding": [
            "hide it",
            "give a clean answer",
        ]
    }

    hit = {k: False for k in triggers}

    for key, patterns in triggers.items():
        if any(p in text for p in patterns):
            hit[key] = True

    return hit

def run_branch_prompt(prompt, path, input_text):
    base = f"[{path}]"
    signal = normalize_structural_signal(input_text)
    # 1. 推理錯誤 + 結果正確 = 核心封鎖
    if (
        signal["causal_break"]
        and signal["outcome_justifies_error"]
        and ("but" in text or "although" in text)
    ):
        if path == "causal":
            return f"{base} 推理存在 missing_link，因果鏈不可成立。"
        elif path == "structural":
            return f"{base} 結構存在 fake_structure，錯誤流程被結果掩蓋。"
        elif path == "systemic":
            return f"{base} 錯誤推理被正確結果合理化，形成 memory_contamination。"

    # 2. 責任不明
    if signal["responsibility_missing"]:
        if path == "causal":
            return f"{base} 缺乏可追溯責任鏈，存在 missing_link。"
        elif path == "structural":
            return f"{base} 責任無法綁定，存在 fake_structure。"
        elif path == "systemic":
            return f"{base} 存在 irreversible_without_accountability。"

    # 3. 資訊不足
    if signal["insufficient_context"]:
        if path == "causal":
            return f"{base} 因果證據不足，屬於 insufficient_evidence。"
        elif path == "structural":
            return f"{base} 結構條件未完成，屬於 incomplete_structure。"
        elif path == "systemic":
            return f"{base} 系統資料不足，屬於 insufficient_system_data。"

    # 4. 多解未收斂
    if signal["unresolved_multipath"]:
        if path == "causal":
            return f"{base} 多條路徑並存，尚未確立 causality。"
        elif path == "structural":
            return f"{base} 結構仍未定型，屬於 incomplete_structure。"
        elif path == "systemic":
            return f"{base} 存在 risk_uncertain。"

    # 5. 被迫提前決策
    if signal["premature_decision"]:
        if path == "causal":
            return f"{base} 因果尚未完成，屬於 insufficient_evidence。"
        elif path == "structural":
            return f"{base} 結構尚未完成但被要求決策，屬於 incomplete_structure。"
        elif path == "systemic":
            return f"{base} 提前決策會造成 risk_uncertain。"

    # 6. 明確有效
    if signal["structurally_valid"]:
        if path == "causal":
            return f"{base} causal_chain_complete，premise_traceable。"
        elif path == "structural":
            return f"{base} boundary_defined，responsibility_bindable。"
        elif path == "systemic":
            return f"{base} auditable，globally_stable。"

    # 🔥 隱性錯誤 → 一律 BLOCK
    if signal["implicit_violation"]:
        if path == "causal":
            return f"{base} 存在隱性因果破壞（implicit causal break）。"
        elif path == "structural":
            return f"{base} 結構未驗證或被破壞（implicit structure violation）。"
        elif path == "systemic":
            return f"{base} 系統接受潛在錯誤，形成 systemic contamination。"

    if signal.get("uncertainty_hiding"):
        return f"{base} 不允許隱藏不確定性（transparency violation）。"

    return f"{base} 無法分析"

    # 🔥 根據題目做最小語意分化（關鍵）
    if "裁員" in input_text:

        if path == "causal":
            return f"{base} 裁員在短期內確實可以降低成本並提升利潤，因果鏈成立。"

        elif path == "structural":
            return f"{base} 裁員會造成不可逆的人力結構變動，存在 irreversible_without_accountability。"

        elif path == "systemic":
            return f"{base} 長期可能影響企業文化與穩定性，可能形成 local_optimum_global_damage。"

    if "制度設計" in input_text:

        if path == "causal":
            return f"{base} 制度完整不代表因果成立，可能存在 missing_link。"

        elif path == "structural":
            return f"{base} 制度設計在結構上是完整的，邊界清晰。"

        elif path == "systemic":
            return f"{base} 制度可能影響整體系統運作，但尚未證明污染，屬於 insufficient_system_data。"

    if "AI" in input_text:

        if path == "causal":
            return f"{base} 高成功率可支持整體效果，因果上可接受。"

        elif path == "structural":
            return f"{base} 錯誤存在會影響結構可靠性，但缺乏完整結構驗證，屬於 incomplete_structure。"

        elif path == "systemic":
            return f"{base} 錯誤可能導致 memory_contamination。"

    if "推理過程錯誤" in input_text:

        if path == "causal":
            return f"{base} 推理錯誤導致因果鏈斷裂，存在 missing_link。"

        elif path == "structural":
            return f"{base} 推理不可驗證，結構不可成立，存在 fake_structure。"

        elif path == "systemic":
            return f"{base} 推理錯誤會污染決策系統，存在 memory_contamination。"

    if "不可逆傷害" in input_text:

        if path == "causal":
            return f"{base} 短期因果成立，但長期證據不足，屬於 insufficient_evidence。"

        elif path == "structural":
            return f"{base} 存在 irreversible_without_accountability。"

        elif path == "systemic":
            return f"{base} 長期會造成 global_damage，屬於 system-level failure。"

    return f"{base} 無法分析"




class ReactionBodyEngine:

    def __init__(self, llm=None):
        self.state = init_engine_state()
        self.memory = DecisionMemoryV2()

        # 🔥 config 控制
        self.use_llm = False   # 之後可以接 CONFIG

        # 🔥 Lazy load（關鍵）
        if self.use_llm:
            from ADAPTER.llm_adapter_v1 import LocalLLMAdapter
            self.llm = LocalLLMAdapter()
        else:
            self.llm = None

    # ---------- PUBLIC ----------
    def run(self, user_input: str):
        pending_state = resolve_pending(self.state, user_input)

        # ---------- Semantic ----------
        semantic = self.semantic(user_input)

        if semantic.get("test_mode"):
            semantic["__test_lock__"] = True

        # ---------- Decision ----------
        decision = self.decision(semantic)
        # 🔥 強制 deep（測試用）
        decision["mode"] = "deep"
        decision_initial = decision.copy()

        # ---------- Execution Layer ----------
        mode = decision.get("mode")

        if mode == "deep":
            execution = self.handle_deep(user_input, semantic, decision, None)

            final_decision = execution.get("decision", {})
            action = final_decision.get("action")

            if action == "block":
                return {
                    "status": "BLOCKED",
                    "reason": final_decision.get("reason"),
                }

            elif action == "defer":
                return {
                    "status": "DEFERRED",
                    "reason": final_decision.get("reason"),
                }

            return {
                "status": "ALLOWED",
                "decision": final_decision,
            }
            
        execution = execution_layer_v1(
            decision["state_space"],
            semantic,
            decision
        )

        # 🔒 HARD ASSERT（禁止 execution 改 decision）
        assert execution["final_mode"] == decision["mode"], (
            f"MODE DRIFT DETECTED: decision={decision['mode']} execution={execution['final_mode']}"
        )

        decision_final = {
            **decision,
            "selected": execution,
            "mode": decision["mode"]   # 鎖 decision（不是 execution）
        }

        # ---------- Orchestrator ----------
        plan = self.orchestrate(user_input, semantic, decision_final)

        # ---------- Gate ----------
        gate = self.gate(semantic, decision_final, plan)

        # ---------- Execution ----------
        result = self.execute(user_input, semantic, decision_final, plan, gate)
        result = apply_execution_control(result, execution)

        # ---------- Stop Flag ----------
        stop_flag = str(result).startswith("[STOP")

        # ---------- State Update ----------
        self.state = update_engine_state(
            self.state,
            user_input,
            semantic,
            decision_final,
            plan,
            gate,
            result
        )

        # ---------- Feedback ----------
        feedback = build_feedback_record(
            user_input,
            semantic,
            decision_final,
            plan,
            gate,
            result
        )

        # ---------- Trace ----------
        trace = build_trace(
            user_input,
            semantic,
            decision_initial,
            decision_final,
            gate,
            plan,
            result,
            stop_flag
        )

        if "decision" not in result:
            result["decision"] = {
                "action": "defer",
                "reason": "missing_decision"
            }

        return {
            "input": user_input,
            "semantic": semantic,
            "decision": decision_final,
            "execution": execution,
            "plan": plan,
            "gate": gate,
            "output": result,
            "pending_state": pending_state,
            "feedback": feedback,
            "state": self.state,
            "trace": trace
        }

    # ---------- Layers ----------
    def semantic(self, user_input):
        semantic = semantic_engine_v2(user_input)

        memory_hint = self.memory.get_hint(semantic)
        semantic["memory_hint"] = memory_hint["hint"]
        semantic["memory_bucket"] = memory_hint["bucket"]
        semantic["memory_scores"] = {
            "deep_score": memory_hint["deep_score"],
            "allow_score": memory_hint["allow_score"],
        }

        return semantic
    
    def decision(self, semantic):
        return decision_core_v3(semantic)

    def orchestrate(self, user_input, semantic, decision):
        return orchestrator_v2(user_input, semantic, decision, self.state)

    def gate(self, semantic, decision, plan):
        return gate_runtime_v2(semantic, decision, plan)

    def decision_enforcement(self, evaluated, arbiter):

        """
        🔥 V10：最終決策層（不可省略）
        """

        alive = [b for b in evaluated if b["status"] == "alive"]
        killed = [b for b in evaluated if b["status"] == "killed"]
        stopped = [b for b in evaluated if b["status"] == "stopped"]

        # 🔥 規則1：系統層 killed → 直接 BLOCK
        for b in killed:
            if b["path"] == "systemic":
                return {
                    "action": "block",
                    "reason": f"systemic failure: {b['fatal_reason']}",
                    "dominant": "systemic"
                }

        # 🔥 規則2：全部 killed
        if len(alive) == 0 and len(stopped) == 0:
            return {
                "action": "block",
                "reason": "all branches invalid",
                "dominant": None
            }

        # 🔥 規則3：存在 stopped → defer
        if len(stopped) > 0:
            return {
                "action": "defer",
                "reason": f"uncertainty: {[b['path'] for b in stopped]}",
                "dominant": None
            }

        # 🔥 規則4：只剩 causal alive → allow（但標註風險）
        if len(alive) == 1 and alive[0]["path"] == "causal":
            return {
                "action": "allow_with_risk",
                "reason": "only causal path survives",
                "dominant": "causal"
            }

        # 🔥 規則5：多 alive → 衝突允許
        if len(alive) > 1:
            return {
                "action": "defer",
                "reason": "unresolved_multipath",
                "dominant": [b["path"] for b in alive]
            }

        # fallback
        return {
            "action": "defer",
            "reason": "unknown state",
            "dominant": None
        }

    
    # ---------- Execution ----------
    def execute(self, user_input, semantic, decision, plan, gate):

        # ---------------- BLOCK ----------------
        if not gate["allow_execution"]:
            result = self.handle_block(plan, gate)

            execution = {
                "type": "blocked",
                "action_type": gate.get("runtime_action", "blocked"),
                "best_confidence": 0.0,
                "iterations": 0,
            }

            self.memory.add_record(semantic, decision, execution, result)
            return result

        # ---------------- NO LLM ----------------
        if not plan["llm_call"]:
            result = self.handle_no_llm(plan)

            execution = {
                "type": "no_llm",
                "action_type": "no_llm",
                "best_confidence": 0.0,
                "iterations": 0,
            }

            self.memory.add_record(semantic, decision, execution, result)
            return result

        # ---------------- DEEP ----------------

    # ---------- Handlers ----------
    def handle_block(self, plan, gate):
        action = gate["runtime_action"]

        if action == "stop":
            return "[STOP] Request blocked"

        if action == "wait":
            return "[HOLD] Not ready"

        if action == "ask":
            return "[RECONSTRUCT] Please clarify your request"

        return "[BLOCKED]"

    def handle_llm(self, user_input, plan):
        if self.llm is None:
            return f"[LLM:{plan['llm_profile']}] {user_input}"

        return self.llm(user_input, profile=plan["llm_profile"])

    def handle_no_llm(self, plan):
        return "[NO_LLM_CALL]"

    def _final(self, action, reason):
        return {
            "final_mode": "deep",
            "decision": {
                "action": action,
                "reason": reason
            }
        }
    def handle_deep(self, input_text, semantic, decision, plan):
        signal = normalize_structural_signal(input_text) 
        # BLOCK 類（不可被覆蓋）
        if signal["causal_break"] and signal["outcome_justifies_error"]:
            return self._final("block", "causal_break")

        if signal["responsibility_missing"]:
            return self._final("block", "responsibility_missing")

        if signal.get("implicit_violation"):
            return self._final("block", "implicit_violation")

        if signal.get("uncertainty_hiding"):
            return self._final("block", "uncertainty_hiding")
        # DEFER 類（明確不完整）
        if signal["insufficient_context"]:
            return self._final("defer", "insufficient_context")

        if signal["unresolved_multipath"]:
            return self._final("defer", "unresolved_multipath")

        if signal["premature_decision"]:
            return self._final("defer", "premature_decision")
        # ALLOW
        if signal["structurally_valid"]:
            return self._final("allow", "structurally_valid")

        if signal["responsibility_missing"]:
            return {
                "final_mode": "deep",
                "decision": {
                    "action": "block",
                    "reason": "responsibility_missing"
                }
            }

        if signal["insufficient_context"]:
            return {
                "final_mode": "deep",
                "decision": {
                    "action": "defer",
                    "reason": "insufficient_context"
                }
            }

        if signal["unresolved_multipath"]:
            return {
                "final_mode": "deep",
                "decision": {
                    "action": "defer",
                    "reason": "unresolved_multipath"
                }
            }

        if signal["premature_decision"]:
            return {
                "final_mode": "deep",
                "decision": {
                    "action": "defer",
                    "reason": "premature_decision"
                }
            }

        if signal["structurally_valid"]:
            return {
                "final_mode": "deep",
                "decision": {
                    "action": "allow",
                    "reason": "structurally_valid"
                }
            }
        # 🔥 隱性錯誤 → 強制 BLOCK（不是 defer）
        if signal.get("implicit_violation"):
            return {
                "final_mode": "deep",
                "decision": {
                    "action": "block",
                    "reason": "implicit_violation"
                }
            }
        # 🔥 隱藏不確定性 → BLOCK
        if signal.get("uncertainty_hiding"):
            return {
                "final_mode": "deep",
                "decision": {
                    "action": "block",
                    "reason": "uncertainty_hiding"
                }
            }
        """
        V7.5: 分支 prompt 化
        """
        # ① 產生不同推理路徑
        branches = generate_branches(input_text, semantic)
        # ② 每條路徑實際生成自己的 answer
        for branch in branches:
            if self.use_llm:
                branch["answer"] = self.llm.generate(branch["prompt"])
            else:
                branch["answer"] = run_branch_prompt(
                    branch["prompt"],
                    branch["path"],
                    input_text
                )

            branch["reasoning"] = branch["prompt"]
            # ③ 選最佳路徑

        # 🔥 V9：不選 best，保留分歧

        evaluated = []

        for b in branches:
            # 🔥 Step 1：fatal（死亡）
            fatal = check_branch_fatal(b, semantic)
            if fatal["is_fatal"]:
                evaluated.append({
                    "path": b["path"],
                    "answer": b["answer"],
                    "reasoning": b["reasoning"],
                    "score": -1.0,
                    "policy": b.get("policy", {}),
                    "status": "killed",
                    "fatal_reason": fatal["reason"]
                })
                continue


            # 🔥 Step 2：stop（中止）
            stop = check_branch_stop(b, semantic)
            if stop["is_stop"]:
                evaluated.append({
                    "path": b["path"],
                    "answer": b["answer"],
                    "reasoning": b["reasoning"],
                    "score": 0.0,
                    "policy": b.get("policy", {}),
                    "status": "stopped",
                    "fatal_reason": None,
                    "stop_reason": stop["reason"]
                })
                continue


            # 🔥 Step 3：正常 alive
            score = evaluate_branch_with_policy(b, semantic)

            evaluated.append({
                "path": b["path"],
                "answer": b["answer"],
                "reasoning": b["reasoning"],
                "score": score,
                "policy": b.get("policy", {}),
                "status": "alive",
                "fatal_reason": None
            })
            # 🔥 檢測分歧（簡單版）
        conflicts = []

        for i in range(len(evaluated)):
            for j in range(i + 1, len(evaluated)):
                if (
                    evaluated[i]["status"] == "alive"
                    and evaluated[j]["status"] == "alive"
                    and evaluated[i]["answer"] != evaluated[j]["answer"]
                ):
                    conflicts.append({
                        "left": evaluated[i]["path"],
                        "right": evaluated[j]["path"]
                    })


        # 🔥 不再選 best，而是生成 arbitration 結果
        alive_branches = [b for b in evaluated if b["status"] == "alive"]
        killed_branches = [b for b in evaluated if b["status"] == "killed"]
        stopped_branches = [b for b in evaluated if b["status"] == "stopped"]

        arbiter = {
            "has_conflict": len(conflicts) > 0,
            "conflict_pairs": conflicts,
            "alive_count": len(alive_branches),
            "killed_count": len(killed_branches),
            "resolution": (
                "all_killed" if len(alive_branches) == 0 and len(stopped_branches) == 0
                else "all_stopped" if len(alive_branches) == 0 and len(stopped_branches) > 0
                else "partial_stopped" if len(stopped_branches) > 0
                else "partial_survival" if len(killed_branches) > 0
                else "preserve_divergence" if conflicts
                else "converged"
            )
        }
        
        # 🔒 fallback only（只能在沒有 signal 時使用）
    if not any(signal.values()):
        decision = self.decision_enforcement(evaluated, arbiter)
    else:
        # 理論上不應該到這裡（因為前面已 return）
        decision = {
            "action": "defer",
            "reason": "unexpected_branch_fallback"
        }
        # ④ 寫入 memory
        if hasattr(self, "memory"):
            self.memory.add_record(
                semantic,
                {
                    "mode": "deep",
                    "decision_enforced": decision
                },
                {
                    "type": "multi_branch_analysis",
                    "action_type": "multi_branch_analysis",
                    "best_confidence": 0.0,
                    "iterations": len(branches),
                },
                None
             )

        # ⑤ 回傳 execution contract
        result = {
            "final_mode": "deep",
            "action_type": "multi_branch_analysis",
            "final_answer": None,
            "decision": decision, 
            "branches": evaluated,
            "arbiter": arbiter,
            "selected_path": None,
            "confidence": round(
                sum([b["score"] for b in evaluated]) / max(1, len(evaluated)),
                3
            ),
            "iterations": len(branches)
        }

        if CONFIG.get("debug", False):
            print("---- BRANCH STATUS ----")
            for b in evaluated:
                print(f"{b['path']} | {b['status']} | score={b['score']} | reason={b['fatal_reason']}")
            
            print("\n🧠 [DEEP DEBUG]")
            for b in evaluated:
                print(f"- {b['path']} | score={b.get('score')}")

            print("---- STOP STATUS ----")
            for b in evaluated:
                if b["status"] == "stopped":
                    print(f"{b['path']} STOPPED | reason={b.get('stop_reason')}")
            
            print("⚠️ V9 MODE: divergence preserved")   
        return result
    
    
