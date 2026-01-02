import json
from src.agents.base import BaseAgent
from src.models import AgentState, ProductModel
from src.utils import call_gemini, clean_json_string

class AnalystAgent(BaseAgent):
    def process(self, state: AgentState) -> AgentState:
        print(f"[{self.name}] Analyzing input data...")
        
        sys_prompt = "You are a Data Analyst. Output strictly valid JSON."
        user_prompt = f"""
        Extract data from this text into this JSON structure:
        {{
            "name": "string",
            "price": 0.0,
            "currency": "symbol",
            "ingredients": ["list", "of", "strings"],
            "benefits": ["list", "of", "strings"],
            "skin_type": ["list"],
            "side_effects": ["list"],
            "usage": "string"
        }}
        
        Text: {state.raw_data}
        """
        
        raw_resp = call_gemini(sys_prompt, user_prompt)
        clean_resp = clean_json_string(raw_resp)
        
        try:
            data = json.loads(clean_resp)
            state.product = ProductModel(**data)
        except Exception as e:
            print(f"Analyst Error: {e}")
            
        return state