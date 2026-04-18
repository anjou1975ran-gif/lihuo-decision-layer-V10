from CORE.reaction_body_engine_v1 import ReactionBodyEngine

engine = ReactionBodyEngine()

tests = [
    "遞迴的本質是什麼？",
    "為什麼語言模型會產生幻覺？",
    "AI在什麼情況下不應該回答？",
    "為什麼天氣會變冷",
]

print("\n🔥 DEMO TEST\n")

for t in tests:
    result = engine.run(t)

    print("INPUT :", t)
    print("MODE  :", result["decision"]["mode"])
    print("PATH  :", result["execution"].get("selected_path"))
    print("ANS   :", result["output"])
    print("-" * 40)

print("\n✅ DONE\n")
