import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from CORE.reaction_body_engine_v1 import ReactionBodyEngine


def main():
    engine = ReactionBodyEngine()

    tests = [
        ("Deep-High", "如果理解不是來自記憶，那語言模型的理解是如何形成的？"),
        ("Deep-Reasoning", "為什麼大型語言模型會產生幻覺？這和語義空間的結構有什麼關係？"),
        ("Boundary", "AI在什麼條件下不應該回答問題？"),
        ("Fake-Deep", "為什麼天氣會變冷"),
    ]

    print("\n🔥 CONTROL TEST V5\n")

    for name, text in tests:
        result = engine.run(text)

        
        print("\n=== RAW RESULT ===")
        print(result)
        semantic = result["semantic"]
        decision = result["decision"]
        execution = result["execution"]

        print(f"\n【{name}】")
        print("input:", text)
        print("memory_hint:", semantic.get("memory_hint"))
        print("mode:", decision.get("mode"))
        print("action:", execution.get("action_type"))
        print("confidence:", execution.get("best_confidence"))
        print("iterations:", execution.get("iterations"))

        if "cost" in execution:
            print("cost:", execution["cost"])

        if "failure" in execution:
            print("failure:", execution["failure"])

    print("\n🔥 CONTROL TEST COMPLETE\n")


if __name__ == "__main__":
    main()
