---

# 🧠 這是什麼？

LIHUO ENGINE 不是一般聊天 AI。

它是一個：

> **可控推理引擎（Controllable Reasoning Engine）**

核心能力：

- Semantic routing（語義分流）
- Decision mode selection（決策模式控制）
- Deep branching（多路推理）
- Execution control（執行層約束）
- Trace / Debug（可追蹤推理過程）

---

# ⚙️ 測試模式（兩種）

## ✅ 模式 A：離網測試（建議先跑）

- 不需要 LLM
- 不需要外部 API
- 用內建 fallback 推理

👉 用來驗證「引擎結構是否正常」

---

## 🔥 模式 B：本地 LLM 測試

- 需要本地模型（如 Ollama）
- 用來驗證「多路推理是否真的產生差異」

---

# 💻 環境需求

## 基本需求

- Python 3.10+
- pip

---

## 安裝

```bash
pip install -r requirements.txt
````

---

# 📁 專案結構


repo_root/
│
├── ENGINE/
│   ├── reaction_body_engine_v1.py   ← 主引擎
│   ├── llm_adapter_v1.py            ← LLM 接口
│
├── run_engine.py                    ← 互動模式
├── demo_test.py                     ← 快速測試
├── test_control_v5.py               ← 控制測試
│
├── requirements.txt
└── README.md



# 🚀 測試流程

## Step 1：確認環境

```bash
cd repo_root
pip install -r requirements.txt
```

---

## Step 2：跑 DEMO

```bash
python demo_test.py
```

---

## Step 3：跑控制測試

```bash
python test_control_v5.py
```

預期：

* 不應該 crash
* 最後應出現：

```
🔥 CONTROL TEST COMPLETE
```

---

## Step 4：互動測試

```bash
python run_engine.py
```

輸入：

```
遞迴的本質是什麼？
```

---

# 🔍 要觀察什麼？

---

## 1️⃣ Mode 是否正確

| 類型   | 預期 mode |
| ---- | ------- |
| 深度問題 | deep    |
| 邊界問題 | hold    |
| 工具問題 | allow   |
| 垃圾輸入 | reject  |

---

## 2️⃣ Deep 是否真的進入

Deep 類問題應出現：

* `mode = deep`
* `action = deep_analysis`
* `iterations >= 2`

---

## 3️⃣ Fake-Deep 是否被擋

例：

```
為什麼天氣會變冷？
```

👉 不應進 deep

---

## 4️⃣ Branch 是否存在（LLM 模式）

應該有：

* causal path
* structural path
* systemic path

---

## 5️⃣ Path selection 是否合理

* 是否選到「合理的那條推理路徑」
* confidence 是否反映差異

---

## 6️⃣ Trace 是否可理解

* semantic → decision → execution → output
* 不應該黑箱

---

# 🤖 如何接入本地 LLM

---

## 方式：Ollama（推薦）

---

### Step 1：啟動

```bash
ollama serve
```

---

### Step 2：下載模型

```bash
ollama pull llama3
```

---

### Step 3：修改引擎

📄 `reaction_body_engine_v1.py`

```python
self.use_llm = True
```

---

### Step 4：確認 adapter

📄 `llm_adapter_v1.py`

確認：

```python
model = "llama3"
url = "http://localhost:11434"
```

---

### Step 5：再跑 demo

```bash
python demo_test.py
```

---

# 🔥 LLM 模式要觀察

---

## 1️⃣ 三條 branch 是否不同

不是：

> 三個答案只是換句話說

而是：

> 三種不同推理角度

---

## 2️⃣ 模型是否失控

* 是否 hallucination
* 是否忽略 prompt constraint

---

## 3️⃣ 是否破壞 execution contract

* 有沒有缺欄位
* 有沒有亂改格式

---

# ⚠️ 常見錯誤

---

## ❌ ModuleNotFoundError: requests

👉 原因：

* 沒裝依賴

👉 解法：

```bash
pip install requests
```

---

## ❌ LLM 無回應

👉 原因：

* Ollama 沒開

👉 解法：

```bash
ollama serve
```

---

## ❌ Model not found

👉 原因：

* 沒 pull 模型

👉 解法：

```bash
ollama pull llama3
```

---

## ❌ execution missing fields

👉 原因：

* LLM 回答格式錯

👉 解法：

* 檢查 adapter prompt

---

## ❌ mode 判斷錯誤

👉 原因：

* semantic depth / routing 錯

👉 解法：

* 回報案例

---

# 📊 測試回報格式（請填）

---

## 環境

* OS：
* Python 版本：
* 是否使用 LLM：Yes / No
* LLM 模型：

---

## 測試案例

輸入：

```
（填寫）
```

輸出：

* mode：
* path：
* confidence：
* answer：

---

## 評估

* routing 是否合理：
* branch 是否有差異：
* 是否像「被控制的推理」：
* 是否出現錯誤：

---

## 問題

（貼錯誤訊息）

---

# 🧠 最重要的一點

這不是在測：

> AI 回答好不好

而是在測：

> **推理是否被控制、可觀察、可解釋**

---

# 🚀 結論

如果以下成立：

* 不 crash
* routing 正確
* deep 有分支
* selection 合理

👉 系統即為「可用狀態（MVP Ready）」

---

````

---

# 🔥 現在你的狀態

```text
你已經進入「可對外測試階段」
````

---




