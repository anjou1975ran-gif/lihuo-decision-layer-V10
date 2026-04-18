from CORE.reaction_body_engine_v1 import ReactionBodyEngine

def main():
    engine = ReactionBodyEngine()

    print("\n🔥 LIHUO ENGINE v0.8 READY")
    print("type 'exit' to quit\n")

    while True:
        user_input = input(">>> ")

        if user_input.lower() in ["exit", "quit"]:
            print("bye.")
            break

        result = engine.run(user_input)

        print("\n--- RESULT ---")
        print("mode       :", result["decision"]["mode"])
        print("answer     :", result["output"])
        print("path       :", result["execution"].get("selected_path"))
        print("confidence :", result["execution"].get("confidence"))

        print("-------------\n")


if __name__ == "__main__":
    main()
