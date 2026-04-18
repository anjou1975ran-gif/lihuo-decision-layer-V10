BRANCH_POLICIES = {

    "causal": {
        "valid_claim": [
            "causal_chain_complete",
            "premise_traceable",
            "counterfactual_stable"
        ],

        "fatal_error": [
            "missing_link",
            "narrative_fill",
            "causal_jump"
        ],

        "stop_condition": [
            "cannot_establish_causality",
            "insufficient_evidence"
        ],

        "reversibility": "medium"
    },

    "structural": {
        "valid_claim": [
            "boundary_defined",
            "reversible",
            "responsibility_bindable"
        ],

        "fatal_error": [
            "irreversible_without_accountability",
            "fake_structure",
            "no_stop_condition"
        ],

        "stop_condition": [
            "structure_not_maintainable",
            "boundary_not_defined",
            "incomplete_structure"
        ],

        "reversibility": "high"
    },

    "systemic": {
        "valid_claim": [
            "no_downstream_pollution",
            "auditable",
            "globally_stable"
        ],

        "fatal_error": [
            "memory_contamination",
            "policy_leak",
            "local_optimum_global_damage",
            "global_damage",              # 🔥 加這行
            "system-level failure"        # 🔥 加這行
        ],

        "stop_condition": [
            "systemic_risk_detected",
            "risk_uncertain",
            "insufficient_system_data"
        ],

        "reversibility": "low"
    }
}
