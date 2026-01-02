from src.models import AgentState
from src.agents.analyst import AnalystAgent
from src.agents.strategist import StrategistAgent
from src.agents.publisher import PublisherAgent

class Orchestrator:
    def __init__(self):
        self.analyst = AnalystAgent("Analyst")
        self.strategist = StrategistAgent("Strategist")
        self.publisher = PublisherAgent("Publisher")

    def run(self, raw_text: str):
        # Step 1: Initialize State
        state = AgentState(raw_data=raw_text)
        
        # Step 2: Sequential Execution (DAG)
        state = self.analyst.process(state)
        
        if not state.product:
            print("Failed to parse product.")
            return {}

        state = self.strategist.process(state)
        state = self.publisher.process(state)
        
        return state.final_json_outputs