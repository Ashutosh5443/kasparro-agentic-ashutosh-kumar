# Kasparro AI Agentic Content System
**Author:** [Your Name]

## 1. Problem Statement
To design a modular, multi-agent automation system that transforms unstructured product data into structured, machine-readable JSON content pages (FAQ, Comparison, Product Page) without relying on a monolithic script.

## 2. Solution Overview
The solution implements a **State-Based Orchestration Architecture**. A central `ContentOrchestrator` manages a shared `AgentState` object which flows through a Directed Acyclic Graph (DAG) of specialized agents.


## 3. System Design
### [cite_start]A. Agent Boundaries 
* **AnalystAgent:** Responsibility is strictly **Domain Modeling**. It converts raw string data into a validated `ProductModel` (Pydantic).
* **StrategistAgent:** Responsibility is **Content Expansion**. It generates synthetic questions and structures competitor data.
* **PublisherAgent:** Responsibility is **Formatting & Assembly**. It uses the Template Engine and Logic Blocks to finalize output.

### [cite_start]B. Logic Blocks 
To avoid "LLM Hallucination" for safety-critical data, I implemented deterministic logic in `src/logic_blocks.py`:
* `generate_safety_warning()`: Scans input for keywords (e.g., "tingling") and appends mandatory medical warnings.
* `compare_ingredients()`: Uses Python Set operations to mathematically find ingredient overlaps.

### [cite_start]C. Template Engine 
I designed a custom `BaseTemplate` class in `src/templates.py`. This enforces a contract where every page type (FAQ, Comparison) has a predefined schema that data must fit into before generation, ensuring the output is always machine-readable JSON.

## 4. Scopes & Assumptions
* **Input Data:** Assumed to be the "GlowBoost" dataset provided.
* **Competitor:** "Product B" is synthetically generated with a fixed structure to ensure comparison logic works reliably.

graph TD
    %% Nodes
    Input[("Raw Product Data\n(Text)")]
    Orchestrator{{"Content Orchestrator\n(System Brain)"}}
    State[("Shared AgentState\n(Pydantic Model)")]
    
    subgraph Agents [Independent Worker Agents]
        Analyst["Analyst Agent\n(Parser)"]
        Strategist["Strategist Agent\n(Planner)"]
        Publisher["Publisher Agent\n(Formatter)"]
    end

    subgraph Logic [Reusable Logic Blocks]
        SafetyLogic("Safety Rules Engine\n(extract_safety_warning)")
        CompLogic("Math Comparison Engine\n(compare_ingredients)")
    end

    subgraph Templates [Template Engine]
        FAQTemp["FAQ Template"]
        CompTemp["Comparison Template"]
    end

    Output[("Final JSON Files\n(faq.json, comparison.json)")]

    %% Flow
    Input --> Orchestrator
    Orchestrator -- "1. Initialize" --> State
    
    Orchestrator -- "2. Parse" --> Analyst
    Analyst -- "Update Model" --> State
    
    Orchestrator -- "3. Plan Content" --> Strategist
    Strategist -- "Add Questions/Competitor" --> State
    
    Orchestrator -- "4. Assemble" --> Publisher
    
    Publisher -.-> SafetyLogic
    Publisher -.-> CompLogic
    Publisher -.-> Templates
    
    Publisher -- "Finalize" --> State
    State --> Output

    %% Styling
    style Orchestrator fill:#f9f,stroke:#333,stroke-width:2px
    style State fill:#ccf,stroke:#333,stroke-width:2px


### Resilience & Fault Tolerance
To ensure production reliability, I implemented a **Circuit Breaker / Fallback Mechanism** in the API layer.
- **Primary Strategy**: Attempt to generate content using the Google Gemini 1.5 Flash model.
- **Fallback Strategy**: If the API encounters Rate Limits (429) or Availability errors (404/500), the system automatically degrades gracefully to use structured mock data. This ensures the pipeline never crashes and always produces valid JSON deliverables.