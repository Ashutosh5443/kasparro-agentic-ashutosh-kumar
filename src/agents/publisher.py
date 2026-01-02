from src.agents.base import BaseAgent
from src.models import AgentState
from src.templates import FAQTemplate, ComparisonTemplate
from src.logic_blocks import generate_safety_warning, compare_ingredients

class PublisherAgent(BaseAgent):
    def process(self, state: AgentState) -> AgentState:
        print(f"[{self.name}] Publishing content...")
        
        # 1. FAQ Page
        faq_tmpl = FAQTemplate(["name", "qs"])
        faq_json = faq_tmpl.render({
            "name": state.product.name,
            "qs": state.generated_questions[:5]
        })
        
        # 2. Comparison Page (Using Logic Block)
        comp_tmpl = ComparisonTemplate(["us", "them", "analysis"])
        ing_analysis = compare_ingredients(state.product.ingredients, state.competitor.ingredients)
        comp_json = comp_tmpl.render({
            "us": state.product.name,
            "them": state.competitor.name,
            "analysis": {
                "ingredients": ing_analysis,
                "price_diff": f"{state.product.price} vs {state.competitor.price}"
            }
        })
        
        # 3. Product Page (Using Logic Block)
        safety = generate_safety_warning(state.product.side_effects, state.product.skin_type)
        prod_json = {
            "title": state.product.name,
            "safety_label": safety,
            "details": state.product.dict()
        }

        state.final_json_outputs = {
            "faq.json": faq_json,
            "comparison.json": comp_json,
            "product_page.json": prod_json
        }
        return state