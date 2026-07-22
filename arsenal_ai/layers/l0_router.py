"""L0: Prompt Report Taxonomy Router.

Analyzes the raw task and classifies it according to the 58-technique 
taxonomy from 'The Prompt Report', dynamically deciding which architectural 
layers (L1-L6) to activate for optimal Cognitive Economy.
"""
from loguru import logger
from arsenal_ai.core.models import ArsenalConfig, TaskSpec, L0RouteDecision
from arsenal_ai.engine.llm import agenerate_structured

class TaxonomyRouter:
    def __init__(self, config: ArsenalConfig):
        self.config = config

    async def route(self, task: TaskSpec) -> L0RouteDecision:
        logger.info(f"🚦 [L0 Router] Analyzing epistemic complexity for Task: {task.task_id}")
        
        messages = [
            {
                "role": "system", 
                "content": (
                    "You are the L0 Taxonomy Router based on 'The Prompt Report' (arXiv:2406.06608). "
                    "Analyze the task and determine the complexity. If the task requires deep reasoning, "
                    "activate L3 (Tree Search) and L4 (Refine). Choose the appropriate prompt families."
                )
            },
            {"role": "user", "content": f"Task Modality: {task.modality.value}\nConstraints: {task.constraints}\nDescription: {task.description}"}
        ]
        
        decision: L0RouteDecision = await agenerate_structured(
            messages=messages,
            response_model=L0RouteDecision,
            model=self.config.target_model,
            api_base=self.config.api_base,
            api_key=self.config.api_key
        )
        
        logger.success(f"🚦 [L0 Router] Route established. Complexity: {decision.complexity_score:.2f} | L3 Active: {decision.activate_l3_search}")
        return decision
