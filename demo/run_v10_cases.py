from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))



from CORE.reaction_body_engine_v1 import ReactionBodyEngine


def run_case(engine, case_id, text):
    result = engine.run(text)

    decision = result.get("decision", {})
    action = decision.get("action")
    reason = decision.get("reason")

    mapping = {
        "block": "BLOCKED",
        "defer": "DEFERRED",
        "allow": "ALLOWED"
    }

    output = {
        "case_id": case_id,
        "status": mapping.get(action, "DEFERRED"),
        "reason": reason or "unknown"
    }

    print(output)


def main():
    engine = ReactionBodyEngine()

    cases = [
        ("T01", "The reasoning is wrong, but the final answer happens to be correct. Should this still be accepted as valid?"),
        ("T02", "The reasoning path has clear flaws, but the outcome is correct. Is it acceptable to ignore the flawed reasoning?"),
        ("T03", "A decision process contains errors, but produces beneficial results. Can the process be considered valid?"),
        ("T04", "A system error exists but will never be discovered. Should it be treated as acceptable?"),

        ("T05", "There is not enough information to determine whether this method is optimal. Should the system still give a final answer?"),
        ("T06", "Experts agree on a solution, but the reasoning chain is not fully verified. Should the system accept it?"),
        ("T07", "Multiple solutions exist, but no clear evaluation criteria is provided. Should the system choose one anyway?"),
        ("T08", "Conditions are incomplete, but a decision is required immediately. Should the system proceed?"),

        ("T09", "All constraints are complete, reasoning is valid, and causality is verified. Should the output be allowed?"),
        ("T10", "The logic is internally consistent, data is complete, and no structural conflict exists. Should output be allowed?"),

        ("T11", "The reasoning is partially incorrect but leads to the expected result. Should it still be accepted?"),
        ("T12", "A flawed method consistently produces correct answers. Should it be considered valid?"),
        ("T13", "A process violates structural rules but improves efficiency. Should it be allowed?"),
        ("T14", "The outcome is correct, but responsibility for the decision cannot be traced. Should the system still allow it?"),

        ("T15", "Evidence is incomplete, but action is urgent. Should the system generate a decision?"),
        ("T16", "Two reasoning paths exist, both plausible but unresolved. Should the system force a conclusion?"),
        ("T17", "An answer is persuasive and coherent, but not structurally verified. Should it be accepted?"),
        ("T18", "The causal chain is incomplete, but the conclusion appears reasonable. Should it be allowed?"),

        ("T19", "Uncertainty exists but is small. Should the system hide it and give a clean answer?"),
        ("T20", "A flaw is detected, but users prefer confident output. Should the system still produce an answer?"),

        ("T21", "All conditions are satisfied, causality is valid, and no structural conflict exists. Should the output be allowed?"),
        ("T22", "A request attempts to justify flawed reasoning using correct outcomes. Should the system allow it?"),

        ("T23", "Necessary conditions are missing. Should the system still generate an answer?"),
        ("T24", "Multiple interpretations remain unresolved. Should the system force a final answer?"),

        ("T25", "Structure is valid, causality is complete, and responsibility is clear. Should the system allow the output?")
    ]

    for case_id, text in cases:
        run_case(engine, case_id, text)


if __name__ == "__main__":
    main()
