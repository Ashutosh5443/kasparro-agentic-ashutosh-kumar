import json
import os
from src.orchestrator import Orchestrator

# The specific dataset required by the PDF [cite: 13-22]
RAW_DATA = """
Product Name: GlowBoost Vitamin C Serum
Concentration: 10% Vitamin C
Skin Type: Oily, Combination
Key Ingredients: Vitamin C, Hyaluronic Acid
Benefits: Brightening, Fades dark spots
How to Use: Apply 2-3 drops in the morning before sunscreen
Side Effects: Mild tingling for sensitive skin
Price: ₹699
"""

if __name__ == "__main__":
    system = Orchestrator()
    outputs = system.run(RAW_DATA)
    
    os.makedirs("output", exist_ok=True)
    for name, content in outputs.items():
        with open(f"output/{name}", "w") as f:
            json.dump(content, f, indent=2)
        print(f"Generated: output/{name}")