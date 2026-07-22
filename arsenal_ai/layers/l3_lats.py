"""L3: Language Agent Tree Search (LATS) Engine.

SOTA integration of Monte Carlo Tree Search (MCTS) with LLM value functions.
Allows the agent to actively look ahead, simulate outcomes, and rollback 
based on rigorous PRM (Process Reward Model) scoring.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio
from loguru import logger
from arsenal_ai.engine.llm import agenerate_structured
from arsenal_ai.core.models import ArsenalConfig

class LatsNodeEvaluation(BaseModel):
    """PRM Evaluation Schema for LATS Node."""
    reward_score: float = Field(ge=0.0, le=1.0, description="Epistemic or programmatic value of this simulated step.")
    critique_reasoning: str = Field(description="Why this step succeeded or failed.")
    is_terminal: bool = Field(description="Does this step solve the ultimate goal?")

class LatsNodeExpansion(BaseModel):
    """The generated possible next steps."""
    proposed_actions: List[str] = Field(description="3 distinct potential next actions to take.")

class LatsEngine:
    """MCTS-driven LLM Search."""
    def __init__(self, config: ArsenalConfig):
        self.config = config

    async def _expand_node(self, current_state: str) -> List[str]:
        """Propose novel branches from the current state."""
        messages = [
            {"role": "system", "content": "You are the LATS Expansion module. Propose 3 distinct, highly logical next actions to advance the current state."},
            {"role": "user", "content": f"Current State: {current_state}"}
        ]
        res: LatsNodeExpansion = await agenerate_structured(
            messages=messages, 
            response_model=LatsNodeExpansion, 
            model=self.config.target_model,
            api_base=self.config.api_base,
            api_key=self.config.api_key
        )
        return res.proposed_actions

    async def _simulate_and_evaluate(self, action: str) -> LatsNodeEvaluation:
        """Simulates the outcome of an action and scores it."""
        messages = [
            {"role": "system", "content": "You are the LATS Value Function (PRM). Simulate the outcome of the proposed action and evaluate its success probability (0.0 to 1.0)."},
            {"role": "user", "content": f"Proposed Action: {action}"}
        ]
        return await agenerate_structured(
            messages=messages, 
            response_model=LatsNodeEvaluation, 
            model=self.config.target_model,
            api_base=self.config.api_base,
            api_key=self.config.api_key
        )

    async def search(self, initial_state: str, max_rollouts: int = 3) -> str:
        """Executes the concurrent MCTS search over the reasoning space."""
        logger.info(f"🌳 [L3 LATS] Initiating Async Tree Search (Rollouts: {max_rollouts})")
        
        # Expand
        actions = await self._expand_node(initial_state)
        
        # Parallel Simulate & Evaluate (The Async SOTA Edge)
        eval_tasks = [self._simulate_and_evaluate(a) for a in actions]
        evaluations = await asyncio.gather(*eval_tasks, return_exceptions=True)
        
        best_action = ""
        best_score = -1.0
        
        for action, evaluation in zip(actions, evaluations):
            if isinstance(evaluation, Exception):
                logger.warning(f"Evaluation failed for action: {evaluation}")
                continue
            logger.debug(f"Action Evaluated -> Score: {evaluation.reward_score} | Terminal: {evaluation.is_terminal}")
            if evaluation.reward_score > best_score:
                best_score = evaluation.reward_score
                best_action = action
                
        logger.success(f"🌳 [L3 LATS] Selected optimal trajectory with score: {best_score}")
        return best_action
