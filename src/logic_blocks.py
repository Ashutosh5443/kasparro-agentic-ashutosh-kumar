"""
Deterministic rules. NO AI here.
Requirement: 'transform data into copy' via rules.
"""

def generate_safety_warning(side_effects: list, skin_types: list) -> str:
    # Logic: If 'tingling' exists, mandate a patch test.
    warnings = []
    text_blob = (" ".join(side_effects) + " " + " ".join(skin_types)).lower()

    if "tingling" in text_blob or "burning" in text_blob:
        warnings.append("PATCH TEST REQUIRED")
    if "sensitive" in text_blob:
        warnings.append("CONSULT DERMATOLOGIST")
    
    return " | ".join(warnings) if warnings else "Standard Safety Protocols Apply"

def compare_ingredients(prod_a: list, prod_b: list) -> dict:
    # Logic: Set theory intersection
    set_a = set(prod_a)
    set_b = set(prod_b)
    return {
        "common": list(set_a.intersection(set_b)),
        "unique_to_us": list(set_a - set_b)
    }