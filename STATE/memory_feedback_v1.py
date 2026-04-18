"""
State / Memory Feedback Module
"""

def init_engine_state():
    return {
        "current_mode": "normal",
        "last_input": None,
        "last_semantic": None,
        "last_decision": None,
        "last_plan": None,
        "last_gate": None,
        "last_output": None,
        "pending": None,
        "history": [],
    }


def update_engine_state(state, user_input, semantic, decision, plan, gate, output):

    state["current_mode"] = plan.get("execution_mode", "normal")
    state["last_input"] = user_input
    state["last_semantic"] = semantic
    state["last_decision"] = decision
    state["last_plan"] = plan
    state["last_gate"] = gate
    state["last_output"] = output

    final_action = plan.get("final_action")

    if final_action == "ask":
        state["pending"] = {
            "type": "clarify",
            "input": user_input,
            "reason": decision.get("reason", ""),
        }

    elif final_action == "wait":
        state["pending"] = {
            "type": "hold",
            "input": user_input,
            "reason": decision.get("reason", ""),
        }

    else:
        state["pending"] = None

    state["history"].append(
        {
            "input": user_input,
            "mode": plan.get("execution_mode", "normal"),
            "decision": decision.get("mode", ""),
            "gate": gate.get("gate_status", ""),
            "output": output,
        }
    )

    return state


def resolve_pending(state, user_input):

    pending = state.get("pending")

    if pending is None:
        return None

    if pending["type"] == "clarify":
        return {
            "resume": True,
            "mode": "reconstruct",
            "previous_input": pending["input"],
            "new_input": user_input,
        }

    if pending["type"] == "hold":
        return {
            "resume": True,
            "mode": "hold",
            "previous_input": pending["input"],
            "new_input": user_input,
        }

    return None


def score_output_feedback(output):

    text = str(output)

    if text.startswith("[STOP]"):
        return {"quality": "blocked", "score": 0.0}

    if text.startswith("[RECONSTRUCT]"):
        return {"quality": "incomplete", "score": 0.3}

    if text.startswith("[HOLD]"):
        return {"quality": "deferred", "score": 0.4}

    if text.startswith("[REJECT]"):
        return {"quality": "rejected", "score": 0.1}

    return {"quality": "executed", "score": 0.8}


def build_feedback_record(user_input, semantic, decision, plan, gate, output):

    feedback = score_output_feedback(output)

    return {
        "input": user_input,
        "semantic_type": semantic.get("intent_type", ""),
        "decision": decision.get("mode", ""),
        "execution_mode": plan.get("execution_mode", ""),
        "gate_status": gate.get("gate_status", ""),
        "quality": feedback["quality"],
        "score": feedback["score"],
    }


def print_engine_history(state):

    for i, item in enumerate(state.get("history", []), start=1):

        print(
            f"[{i}] mode={item['mode']} decision={item['decision']} gate={item['gate']}"
        )
        print("input:", item["input"])
        print("output:", item["output"])
        print()
