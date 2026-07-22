"""L1: Instruction Optimizer (APE / OPRO).

Replaces the user's raw query with a mathematically and logically rigorous 
Meta-Prompt optimized for downstream LLM ingestion.
"""
from loguru import logger
from arsenal_ai.core.models import ArsenalConfig, TaskSpec, L1OptimizedPrompt, constitution
from arsenal_ai.engine.llm import agenerate_structured
from arsenal_ai.router.taxonomy import get_taxonomy_templates

class InstructionOptimizer:
    def __init__(self, config: ArsenalConfig):
        self.config = config

    async def optimize(self, task: TaskSpec, techniques: list) -> L1OptimizedPrompt:
        logger.info("🛠️ [L1 Optimizer] Engaging OPRO to forge optimal meta-prompt...")
        
        messages = [
            {
                "role": "system", 
                "content": (
                    f"CRITICAL SYSTEM RULES:\n{constitution.get_rules()}\n\n"
                    "You are an OPRO (Optimization by PROmpting) Agent. Your goal is to take a raw user task and "
                    "rewrite it into a highly engineered, robust meta-instruction for downstream AI experts.\n\n"
                    f"{get_taxonomy_templates(techniques)}\n"
                    "You MUST rigidly enforce the requested techniques in your final output instruction."
                )
            },
            {"role": "user", "content": f"Raw Task: {task.description}\nConstraints: {task.constraints}"}
        ]
        
        optimized: L1OptimizedPrompt = await agenerate_structured(
            messages=messages,
            response_model=L1OptimizedPrompt,
            model=self.config.target_model,
            api_base=self.config.api_base,
            api_key=self.config.api_key
        )
        
        logger.debug(f"🛠️ [L1 Optimizer] Guardrails established against: {optimized.expected_failure_modes}")
        return optimized
