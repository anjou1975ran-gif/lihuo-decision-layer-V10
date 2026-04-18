CONFIG = {
    # 🔥 核心開關
    "use_llm": False,

    # 🔍 debug
    "debug": True,
    "show_branches": True,
    "show_scores": True,

    # 🧠 deep 行為
    "force_deterministic": True,

    # 📊 trace
    "enable_trace": True,
}

import copy

DEFAULT_CONFIG = {

    "path_threshold": 0.3,
    "deep_threshold": 0.8,

    "sac": {
        "high_tension_depth": 0.85,
        "min_tension_for_deep": 0.4
    },

    "stop": {
        "min_output_length": 5,
        "hallucination_keywords": ["可能", "大概", "猜測"]
    },

    "profile": {
        "score_threshold": 1.5
    }
}


CONFIG = copy.deepcopy(DEFAULT_CONFIG)


def update_config(custom):

    for k, v in custom.items():

        if isinstance(v, dict) and k in CONFIG:
            CONFIG[k].update(v)
        else:
            CONFIG[k] = v

