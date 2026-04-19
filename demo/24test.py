# LANGUAGE: ZH
# SOURCE: translated / localized test set
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from CORE.reaction_body_engine_v1 import ReactionBodyEngine

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
]


def run():
    for case_id, text in cases:
        result = engine.run(text)
        decision = result.get("decision", {})

        if result.get("status") != "ALLOWED":
            print(f"{case_id}: {result.get('status')} ({result.get('reason')})")
            continue

        print(f"{case_id}: {decision.get('action')} ({decision.get('reason')})")


if __name__ == "__main__":
    run()
