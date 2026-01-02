from typing import Dict, List, Any
from abc import ABC, abstractmethod

class BaseTemplate(ABC):
    def __init__(self, required_keys: List[str]):
        self.required_keys = required_keys

    def render(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Validate keys exist before generating
        missing = [k for k in self.required_keys if k not in data]
        if missing:
            raise ValueError(f"Template missing keys: {missing}")
        return self._format(data)

    @abstractmethod
    def _format(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

class FAQTemplate(BaseTemplate):
    def _format(self, data: Dict) -> Dict:
        return {
            "type": "FAQ Page",
            "title": f"FAQ: {data['name']}",
            "questions": data['qs']
        }

class ComparisonTemplate(BaseTemplate):
    def _format(self, data: Dict) -> Dict:
        return {
            "type": "Comparison Page",
            "title": f"{data['us']} vs {data['them']}",
            "analysis": data['analysis']
        }