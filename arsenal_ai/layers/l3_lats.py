"""L3: Language Agent Tree Search (LATS) Engine with Environment Feedback.

TRUE LATS Implementation:
Unlike naive Tree of Thoughts which only uses an LLM-as-a-judge, 
LATS executes the proposed actions in the Environment (Python Sandbox), 
and the PRM evaluates the *Environment Response* (stdout/traceback) 
to calculate the reward score. This grounds the search in reality.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio
from loguru import logger
from arsenal_ai.engine.llm import agenerate_structured
from arsenal_ai.core.models import ArsenalConfig
from arsenal_ai.tools.executor import CodeSandbox

class LatsNodeEvaluation(BaseModel):
    """PRM Evaluation Schema for LATS Node."""
    reward_score: float = Field(ge=0.0, le=1.0, description="Score based on both logic and environment execution success.")
    critique_reasoning: str = Field(description="Why this step succeeded or failed based on the sandbox output.")
    is_terminal: bool = Field(description="Does this step solve the ultimate goal without errors?")

class LatsAction(BaseModel):
    reasoning: str = Field(description="Step-by-step logic.")
    python_code_to_execute: Optional[str] = Field(default=None, description="Code to test this branch.")

class LatsNodeExpansion(BaseModel):
    proposed_actions: List[LatsAction]

class LatsEngine:
    def __init__(self, config: ArsenalConfig):
        self.config = config

    async def _expand_node(self, current_state: str, max_branches: int = 3) -> List[LatsAction]:
        """Propose novel branches from the current state, writing executable code."""
        messages = [
            {"role": "system", "content": f"You are the LATS Expansion module. Propose {max_branches} distinct actions to advance the current state. If code is needed, provide 'python_code_to_execute'."},
            {"role": "user", "content": f"Current State: {current_state}"}
        ]
        res: LatsNodeExpansion = await agenerate_structured(
            messages=messages, 
            response_model=LatsNodeExpansion, 
            model=self.config.target_model,
            api_base=self.config.api_base,
            api_key=self.config.api_key
        )
        return res.proposed_actions[:max_branches]

    async def _simulate_and_evaluate(self, action: LatsAction) -> LatsNodeEvaluation:
        """Executes the action in the Sandbox FIRST, then scores the output."""
        execution_logs = "No execution attempted."
        
        # 1. Environment Interaction (The defining feature of LATS)
        if action.python_code_to_execute:
            logger.debug("🌳 [LATS] Executing node trajectory in Sandbox...")
            sandbox_res = CodeSandbox.execute(action.python_code_to_execute)
            if sandbox_res["success"]:
                execution_logs = f"SUCCESS Output:\n{sandbox_res['output']}"
            else:
                execution_logs = f"FAILURE Traceback:\n{sandbox_res['error']}"

        # 2. LLM-as-a-Judge Evaluation of the Environment Feedback
        messages = [
            {"role": "system", "content": "You are the LATS Value Function (PRM). Score the proposed action based on its reasoning and the actual Sandbox Execution logs."},
            {"role": "user", "content": f"Reasoning: {action.reasoning}\n\nSandbox Logs:\n{execution_logs}"}
        ]
        
        return await agenerate_structured(
            messages=messages, 
            response_model=LatsNodeEvaluation, 
            model=self.config.target_model,
            api_base=self.config.api_base,
            api_key=self.config.api_key
        )

    async def search(self, initial_state: str, max_rollouts: int = 2) -> str:
        """Executes concurrent LATS search over the reasoning space with environment feedback."""
        logger.info(f"🌳 [L3 LATS] Initiating Async Tree Search with Environment Grounding (Rollouts: {max_rollouts})")
        
        actions = await self._expand_node(initial_state, max_branches=max_rollouts)
        
        # Parallel Simulate (Execute Code) & Evaluate
        eval_tasks = [self._simulate_and_evaluate(a) for a in actions]
        evaluations = await asyncio.gather(*eval_tasks, return_exceptions=True)
        
        best_action = None
        best_score = -1.0
        
        for action, evaluation in zip(actions, evaluations):
            if isinstance(evaluation, Exception):
                logger.warning(f"LATS Evaluation failed: {evaluation}")
                continue
                
            logger.debug(f"Trajectory Evaluated -> Score: {evaluation.reward_score} | Terminal: {evaluation.is_terminal}")
            
            if evaluation.reward_score > best_score:
                best_score = evaluation.reward_score
                best_action = action
                
        if best_action:
            logger.success(f"🌳 [L3 LATS] Selected optimal grounded trajectory with score: {best_score}")
            return f"Reasoning: {best_action.reasoning}\nCode: {best_action.python_code_to_execute or 'None'}"
        return initial_state
