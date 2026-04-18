

## I. OpenAI Adapter

```python
class OpenAIAdapter:

    def __init__(self, client, model="gpt-4o-mini"):
        self.client = client
        self.model = model

    def __call__(self, prompt, profile="surface"):

        system_prompt = self.build_system_prompt(profile)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content
```

---

## II. System Prompt Builder

```python
    def build_system_prompt(self, profile):

        if profile == "surface":
            return "Answer directly and concisely."

        if profile == "structural":
            return "Break down the structure and explain step by step."

        if profile == "boundary":
            return "Answer in strict structural terms. Avoid emotional or human-like language."

        if profile == "reflective":
            return "Reflect on the meaning and reasoning process before answering."

        if profile == "co_constructive":
            return "Collaboratively build the answer with the user."

        return "Answer normally."
```

---

## III. Local LLM Adapter（通用）

```python
class LocalLLMAdapter:

    def __init__(self, model_callable):
        self.model = model_callable

    def __call__(self, prompt, profile="surface"):

        prefix = self.build_prefix(profile)

        return self.model(prefix + "\n" + prompt)
```

---

## IV. Prefix Builder

```python
    def build_prefix(self, profile):

        if profile == "surface":
            return "[MODE: DIRECT ANSWER]"

        if profile == "structural":
            return "[MODE: STRUCTURE ANALYSIS]"

        if profile == "boundary":
            return "[MODE: STRICT STRUCTURAL / NO HUMANIZATION]"

        if profile == "reflective":
            return "[MODE: REFLECTIVE THINKING]"

        if profile == "co_constructive":
            return "[MODE: CO-CONSTRUCTION]"

        return "[MODE: NORMAL]"
```

---

## V. Engine Integration（改這一段）

```python
def handle_llm(self, user_input, plan):

    if self.llm is None:
        return "[LLM_CALL] " + user_input

    return self.llm(user_input)
```

---

## 👉 改成：

```python
def handle_llm(self, user_input, plan):

    profile = plan.get("llm_profile", "surface")

    if self.llm is None:
        return f"[LLM_CALL:{profile}] {user_input}"

    return self.llm(user_input, profile=profile)
```

---

## VI. Usage Example

```python
from openai import OpenAI

client = OpenAI()

llm = OpenAIAdapter(client)

engine = ReactionBodyEngine(llm=llm)

print(engine.run("AI為什麼會幻覺？")["output"])
```

---

## VII. Local Example

```python
def fake_local_model(prompt):
    return "[LOCAL MODEL OUTPUT]\n" + prompt

llm = LocalLLMAdapter(fake_local_model)

engine = ReactionBodyEngine(llm=llm)
```

---

## VIII. Lock

```text
LLM Adapter v1 = 模型解耦層（Model Agnostic Interface）
```

---

## IX. Capability Unlock

```text
✔ 可切換任意模型
✔ 可控制輸出風格（profile）
✔ Reaction Body 完整接管輸出行為
```

---

