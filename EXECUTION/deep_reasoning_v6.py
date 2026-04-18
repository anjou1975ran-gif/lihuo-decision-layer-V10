import random

def generate_candidates(prompt: str):
    """
    產生多個推理候選（mock版，之後可接LLM）
    """
    return [
        f"[A] {prompt} → 基礎推理",
        f"[B] {prompt} → 結構推理",
        f"[C] {prompt} → 抽象推理"
    ]


def evaluate_answer(answer: str):
    """
    評分（暫時用 heuristic）
    """
    score = 0.0

    if "結構" in answer:
        score += 0.4
    if "抽象" in answer:
        score += 0.3
    if "基礎" in answer:
        score += 0.2

    # 微隨機避免鎖死
    score += random.uniform(0, 0.1)

    return round(score, 3)


def select_best(candidates):
    scored = [(c, evaluate_answer(c)) for c in candidates]
    best = max(scored, key=lambda x: x[1])

    return {
        "best_answer": best[0],
        "score": best[1],
        "all": scored
    }
