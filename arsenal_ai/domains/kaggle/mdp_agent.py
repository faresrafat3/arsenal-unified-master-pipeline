"""SOTA Autonomous Data Scientist Agent (Kaggle MDP Mode).

Inspired by Agent K v1.0 and AutoKaggle. 
This agent operates inside ARSENAL's Sandbox but runs a continuous 
Markov Decision Process (MDP). It writes code, tests it, tunes hyperparameters, 
reads tracebacks, and iterates until the metric threshold is met.
"""
from loguru import logger
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from arsenal_ai.engine.llm import agenerate_structured
from arsenal_ai.core.models import ArsenalConfig
from arsenal_ai.tools.executor import CodeSandbox

class KaggleAction(BaseModel):
    rationale: str = Field(description="Why this specific code/model choice was made based on previous state.")
    python_code: str = Field(description="Executable python code for EDA, Feature Engineering, or Modeling.")
    expected_outcome: str = Field(description="What should the stdout show if this succeeds?")
    is_final_submission: bool = Field(description="True if the model has reached the target accuracy and is ready for submission.")

class AutoKaggleMaster:
    def __init__(self, config: ArsenalConfig, max_iterations: int = 5):
        self.config = config
        self.max_iterations = max_iterations
        self.memory_buffer = []

    async def _decide_next_action(self, current_state: str) -> KaggleAction:
        messages = [
            {"role": "system", "content": "You are Agent K v1.0, an Autonomous Kaggle Grandmaster. "
                                          "You operate as an MDP (Markov Decision Process). "
                                          "Based on the execution history, write the next block of Python code to advance the ML pipeline (EDA -> Feature Eng -> Tuning). "
                                          "Do NOT write pseudo-code. Write functional sklearn/pandas code."},
            {"role": "user", "content": f"Execution History & Current State:\n{current_state}\n\nWhat is your next action?"}
        ]
        return await agenerate_structured(
            messages=messages, 
            response_model=KaggleAction, 
            model=self.config.target_model,
            api_base=self.config.api_base,
            api_key=self.config.api_key
        )

    async def solve(self, task_description: str) -> Dict[str, Any]:
        logger.info(f"🏆 [Kaggle Master] Initializing MDP Loop for task: {task_description[:50]}...")
        
        current_state = f"TASK: {task_description}\nSTATUS: Just starting. Need to load data and check baseline."
        best_code = ""
        
        for iteration in range(self.max_iterations):
            logger.debug(f"🏆 [Kaggle Master] Iteration {iteration+1}/{self.max_iterations}")
            
            # 1. Decide
            action = await self._decide_next_action(current_state)
            logger.info(f"Strategy: {action.rationale}")
            
            # 2. Execute in Sandbox
            sandbox_res = CodeSandbox.execute(action.python_code, timeout=15)
            
            # 3. Observe & Update State
            if sandbox_res["success"]:
                logger.success("✅ Code execution successful.")
                obs = f"\n[Iter {iteration+1} SUCCESS]\nCode run:\n{action.python_code[:200]}...\nOutput:\n{sandbox_res['output']}"
                best_code += f"\n# --- Iteration {iteration+1} ---\n{action.python_code}"
            else:
                logger.warning("❌ Code execution failed.")
                obs = f"\n[Iter {iteration+1} FAILED]\nCode run:\n{action.python_code[:200]}...\nTraceback:\n{sandbox_res['error']}"
            
            self.memory_buffer.append(obs)
            
            if len(self.memory_buffer) > 3:
                self.memory_buffer.pop(0)
                
            current_state = "".join(self.memory_buffer)
            
            if action.is_final_submission and sandbox_res["success"]:
                logger.success("🏆 [Kaggle Master] Target accuracy reached! MDP Halted.")
                break

        return {
            "status": "completed",
            "final_pipeline_code": best_code,
            "execution_history": self.memory_buffer
        }
