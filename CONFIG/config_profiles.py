from CONFIG.config import update_config


CONFIG_PROFILES = {

    # ---------- DEFAULT ----------
    "default": {
        "path_threshold": 0.3,
        "deep_threshold": 0.8
    },

    # ---------- STRICT ----------
    "strict": {
        "path_threshold": 0.5,
        "deep_threshold": 0.9,
        "stop": {
            "min_output_length": 10
        }
    },

    # ---------- RESEARCH ----------
    "research": {
        "path_threshold": 0.2,
        "deep_threshold": 0.7,
        "sac": {
            "high_tension_depth": 0.75
        }
    },

    # ---------- CREATIVE ----------
    "creative": {
        "path_threshold": 0.1,
        "deep_threshold": 0.6,
        "stop": {
            "hallucination_keywords": []
        }
    }
}


def apply_profile(name):

    profile = CONFIG_PROFILES.get(name)

    if not profile:
        print(f"[ERROR] profile not found: {name}")
        return

    update_config(profile)
    print(f"[PROFILE] switched to: {name}")