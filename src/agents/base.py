from abc import ABC, abstractmethod
from src.models import AgentState

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process(self, state: AgentState) -> AgentState:
        pass