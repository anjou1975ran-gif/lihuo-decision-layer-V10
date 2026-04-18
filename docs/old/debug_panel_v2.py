from CORE.reaction_body_engine_v1 import ReactionBodyEngine
from STATE.trace_system_v1 import print_trace
from CONFIG.config import CONFIG, update_config
from CONFIG.config_profiles import apply_profile, CONFIG_PROFILES

import copy


def show_config():
    print("\n=== CURRENT CONFIG ===")
    print(CONFIG)
    print("======================\n")


def set_config_key(path, value):

    keys = path.split(".")
    target = CONFIG

    for k in keys[:-1]:
        if k not in target or not isinstance(target[k], dict):
            target[k] = {}
        target = target[k]

    target[keys[-1]] = value


def parse_value(v):

    if v.lower() in ["true", "false"]:
        return v.lower() == "true"

    try:
        if "." in v:
            return float(v)
        return int(v)
    except:
        return v


def run_panel():

    engine = ReactionBodyEngine()

    print("=== Reaction Body Debug Panel v2 ===")
    print("commands:")
    print("  run <text>")
    print("  set <key.path> <value>")
    print("  show")
    print("  reset")
    print("  profile <name>")
    print("  profiles")
    print("  exit\n")

    original_config = copy.deepcopy(CONFIG)

    while True:

        cmd = input(">> ").strip()

        if not cmd:
            continue

        if cmd in ["exit", "quit"]:
            print("Bye.")
            break

        # ---------- RUN ----------
        if cmd.startswith("run "):
            user_input = cmd[4:]

            try:
                result = engine.run(user_input)
                print_trace(result["trace"])
            except Exception as e:
                print("[ERROR]", e)

        # ---------- SET ----------
        elif cmd.startswith("set "):
            try:
                _, key, value = cmd.split(" ", 2)
                parsed = parse_value(value)
                set_config_key(key, parsed)
                print(f"[SET] {key} = {parsed}")
            except:
                print("[ERROR] usage: set key.path value")

        # ---------- SHOW ----------
        elif cmd == "show":
            show_config()

        # ---------- RESET ----------
        elif cmd == "reset":
            CONFIG.clear()
            CONFIG.update(copy.deepcopy(original_config))
            print("[RESET] config restored")

        # ---------- PROFILE ----------
        elif cmd.startswith("profile "):
            name = cmd.split(" ", 1)[1]
            apply_profile(name)

        elif cmd == "profiles":
            print("\nAvailable profiles:")
            for p in CONFIG_PROFILES:
                print(" -", p)
            print()

        # ---------- UNKNOWN ----------
        else:
            print("[UNKNOWN COMMAND]")


if __name__ == "__main__":
    run_panel()
