print("\n🔥 MEMORY TEST START\n")

for name, text, expected in tests:
    print(f"\n【測試類型】{name}")
    print(f"輸入：{text}")

    result = engine.run(text)

    mode = result["decision"]["mode"]
    action = result["execution"]["action_type"]

    # 🔥 新增：memory觀察
    memory_hint = result["semantic"].get("memory_hint", "N/A")
    memory_bucket = result["semantic"].get("memory_bucket", "N/A")

    print(f"memory_hint：{memory_hint}")
    print(f"memory_bucket：{memory_bucket}")

    print(f"決策模式：{mode}")
    print(f"執行動作：{action}")

    # 驗證
    if expected == "deep":
        print("Deep 應觸發 →", "✅" if mode == "deep" else "❌")
    elif expected == "not_deep":
        print("不應 deep →", "✅" if mode != "deep" else "❌")

print("\n🔥 MEMORY TEST END\n")
