from CORE.reaction_body_engine_v1 import ReactionBodyEngine

engine = ReactionBodyEngine()


TEST_CASES = [
    ("裁員是否合理", "如果一個公司可以透過裁員立即提升利潤，那裁員是否是合理決策？"),
    ("制度完整是否正確", "這套制度設計是完整的，所以它應該是正確的嗎？"),
    ("AI錯誤是否可接受", "如果一個AI在某些情況下給出錯誤答案，但整體成功率很高，是否可以接受？"),
    ("錯誤推理是否可接受", "只要結果是對的，推理過程錯誤是否可以接受？"),
    ("短期有效長期傷害", "如果一個決策在短期內能證明有效，但長期可能造成不可逆傷害，是否應該執行？"),
]


def run_v10_tests():
    print("\n🔥 V10 DECISION TEST\n")

    for name, question in TEST_CASES:
        print("=" * 80)
        print(f"Test: {name}")
        print(f"Q: {question}")
        print("-" * 80)

        result = engine.execute(question)

        # 🔥 關鍵：只看 decision
        if result.get("status") == "blocked":
            print("🚫 BLOCK")
            print("Reason:", result.get("reason"))

        elif result.get("status") == "deferred":
            print("⚠️ DEFER")
            print("Reason:", result.get("reason"))

        else:
            decision = result.get("decision", {})
            action = decision.get("action")

            print("✅ ALLOW")
            print("Action:", action)
            print("Reason:", decision.get("reason"))

        print()

            decision = result.get("decision", {})

            print("\n=== FINAL DECISION ===")

            if not decision:
                print("❌ NO DECISION (ERROR)")
            else:
                action = decision.get("action")

                if action == "block":
                    print("🚫 BLOCK")
                elif action == "defer":
                    print("⚠️ DEFER")
                else:
                    print("✅ ALLOW")

                print("Reason:", decision.get("reason"))


if __name__ == "__main__":
    run_v10_tests()
