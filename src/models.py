from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# 1. Product Schema
class ProductModel(BaseModel):
    name: str
    price: float
    currency: str
    ingredients: List[str]
    benefits: List[str]
    skin_type: List[str]
    side_effects: List[str]
    usage: str

# 2. Competitor Schema (Product B)
class CompetitorModel(ProductModel):
    is_fictional: bool = True

# 3. The Global State (Passed between agents)
class AgentState(BaseModel):
    raw_data: str
    product: Optional[ProductModel] = None
    competitor: Optional[CompetitorModel] = None
    generated_questions: List[Dict[str, str]] = [] 
    final_json_outputs: Dict[str, Dict] = {}