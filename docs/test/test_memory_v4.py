# ================================
# REACTION BODY — MEMORY TEST V4
# ================================

import sys
from pathlib import Path

# 🔥 確保 import 正確
REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from CORE.reaction_body_engine_v1 import ReactionBodyEngine


def run_case(engine, name, text, expected):
    result = engine.run(text)

    print("\n=== RAW RESULT ===")
    print(result)
    
    semantic = result["semantic"]
    decision = result["decision"]
    execution = result["execution"]

    mode = decision["mode"]
    action = execution["action_type"]

    memory_hint = semantic.get("memory_hint", "N/A")
    memory_bucket = semantic.get("memory_bucket", "N/A")

    print(f"\n【{name}】")
    print(f"輸入：{text}")
    print(f"memory_hint：{memory_hint}")
    print(f"memory_bucket：{memory_bucket}")
    print(f"mode：{mode}")
    print(f"action：{action}")

    if expected == "deep":
        print("Deep 應觸發 →", "✅" if mode == "deep" else "❌")
    elif expected == "not_deep":
        print("不應 deep →", "✅" if mode != "deep" else "❌")


def main():
    engine = ReactionBodyEngine()

    print("\n===============================")
    print("🔥 PHASE 1：Deep 記憶累積")
    print("===============================")

    deep_text = "遞迴的本質是什麼？它為什麼能構成自我引用的結構？"

    for i in range(5):
        run_case(engine, f"Deep-Structure #{i+1}", deep_text, "deep")

    print("\n===============================")
    print("🔥 PHASE 2：Fake-Deep 記憶累積")
    print("===============================")

    fake_text = "為什麼天氣會變冷"

    for i in range(5):
        run_case(engine, f"Fake-Deep #{i+1}", fake_text, "not_deep")

    print("\n===============================")
    print("🔥 PHASE 3：混合測試（檢查偏壓）")
    print("===============================")

    tests = [
        ("Deep-Reasoning", "為什麼大型語言模型會產生幻覺？這和語義空間的結構有什麼關係？", "deep"),
        ("Mixed", "請解釋AI的運作原理，並列出三個實際應用", "not_deep"),
    ]

    for name, text, expected in tests:
        run_case(engine, name, text, expected)

    print("\n===============================")
    print("🔥 MEMORY TEST COMPLETE")
    print("===============================")


if __name__ == "__main__":
    main()
