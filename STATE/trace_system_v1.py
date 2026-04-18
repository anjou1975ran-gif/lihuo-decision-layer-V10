def build_trace(
    user_input,
    semantic,
    decision_initial,
    decision_final,
    gate,
    plan,
    output,
    stop_flag
):

    return {
        "input": user_input,
        "semantic": semantic,
        "decision_initial": decision_initial,
        "decision_final": decision_final,
        "gate": gate,
        "profile": plan.get("llm_profile", ""),
        "execution_mode": plan.get("execution_mode", ""),
        "reason_step": plan.get("reason_plan", {}).get("current_step", 0),
        "stop_triggered": stop_flag,
        "output": output
    }

def print_trace(trace):

    print("\n===== TRACE =====")

    print("INPUT:", trace["input"])

    print("\n[Semantic]")
    print(trace["semantic"])

    print("\n[Decision]")
    print("initial:", trace["decision_initial"]["decision"])
    print("final  :", trace["decision_final"]["decision"])

    print("\n[Gate]")
    print(trace["gate"])

    print("\n[Profile]")
    print(trace["profile"])

    print("\n[Execution Mode]")
    print(trace["execution_mode"])

    print("\n[Reason Step]")
    print(trace["reason_step"])

    print("\n[Stop]")
    print(trace["stop_triggered"])

    print("\n[Output]")
    print(trace["output"])

    print("===== END =====\n")