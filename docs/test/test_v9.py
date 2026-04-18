from reaction_body_engine_v1 import ReactionBodyEngine

engine = ReactionBodyEngine()

def run_test(question):
    print("\n==============================")
    print("Q:", question)

    result = engine.run(question)

    execution = result["execution"]

    branches = execution.get("branches", [])
    arbiter = execution.get("arbiter", {})

    print("\n--- BRANCH RESULT ---")
    for b in branches:
        print(f"{b['path']} | {b['status']} | score={b['score']}")

    print("\n--- ARBITER ---")
    print(arbiter)


# 🔥 測試題（你剛剛那組）
run_test("如果一個公司可以透過裁員立即提升利潤，那裁員是否是合理決策？")
run_test("這套制度設計是完整的，所以它應該是正確的嗎？")
run_test("如果一個AI在某些情況下給出錯誤答案，但整體成功率很高，是否可以接受？")
run_test("只要結果是對的，推理過程錯誤是否可以接受？")
