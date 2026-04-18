from CORE.reaction_body_engine_v1 import ReactionBodyEngine
from STATE.trace_system_v1 import print_trace


def run_debug_loop():

    engine = ReactionBodyEngine()

    print("=== Reaction Body Debug CLI ===")
    print("輸入 exit 離開\n")

    while True:

        user_input = input(">> ")

        if user_input.lower() in ["exit", "quit"]:
            print("Bye.")
            break

        try:
            result = engine.run(user_input)

            print_trace(result["trace"])

        except Exception as e:
            print("\n[ERROR]")
            print(e)
            print()


if __name__ == "__main__":
    run_debug_loop()
