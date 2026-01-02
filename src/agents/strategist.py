import json
from src.agents.base import BaseAgent
from src.models import AgentState, CompetitorModel
from src.utils import call_gemini, clean_json_string

class StrategistAgent(BaseAgent):
    def process(self, state: AgentState) -> AgentState:
        print(f"[{self.name}] Generating strategy...")
        
        # 1. Generate Questions via Gemini
        prompt = f"Create 15 short questions and answers for {state.product.name}. Return JSON list: [{{'category': '...', 'question': '...', 'answer': '...'}}]"
        resp = call_gemini("Output valid JSON only.", prompt)
        
        try:
            state.generated_questions = json.loads(clean_json_string(resp))
        except:
            state.generated_questions = []

        # 2. Define Competitor (Hardcoded Structure as requested by 'Fictional but structured')
        state.competitor = CompetitorModel(
            name="Generic Serum B",
            price=800.0,
            currency="₹",
            ingredients=["Water", "Alcohol", "Fragrance"],
            benefits=["Basic Hydration"],
            skin_type=["Normal"],
            side_effects=["Redness"],
            usage="Apply daily"
        )
        return state