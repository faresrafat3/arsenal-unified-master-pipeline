"""L4: Adversarial Self-Refine (The Crucible).

SOTA implementation of self-correction loops. It critically examines 
the output of L3/L2, tests it for logic/code errors, and aggressively 
rewrites it to perfection.
"""
from pydantic import BaseModel, Field
from typing import List, Tuple
from loguru import logger
from arsenal_ai.engine.llm import agenerate_structured
from arsenal_ai.core.models import ArsenalConfig, TaskSpec

class CritiqueFeedback(BaseModel):
    passes_quality_bar: bool = Field(description="True only if the artifact is flawless.")
    critical_flaws: List[str] = Field(description="Identified bugs, logical leaps, or unaddressed constraints.")

class RefinedDraft(BaseModel):
    improved_content: str = Field(description="The rewritten, flawless artifact.")
    changes_made: List[str] = Field(description="Changelog of what was fixed.")

class SelfRefineCrucible:
    def __init__(self, config: ArsenalConfig):
        self.config = config

    async def _critique(self, task: TaskSpec, draft: str) -> CritiqueFeedback:
        messages = [
            {"role": "system", "content": "You are the L4 Adversarial Critic. Find every flaw, hallucination, or logic error in this draft."},
            {"role": "user", "content": f"Task Constraints: {task.constraints}\n\nDraft:\n{draft}"}
        ]
        return await agenerate_structured(
            messages=messages, response_model=CritiqueFeedback,
            model=self.config.target_model, api_base=self.config.api_base, api_key=self.config.api_key
        )

    async def _rewrite(self, draft: str, critique: CritiqueFeedback) -> RefinedDraft:
        messages = [
            {"role": "system", "content": "You are the L4 Synthesizer. Rewrite the draft to fix all listed flaws perfectly."},
            {"role": "user", "content": f"Original Draft:\n{draft}\n\nFlaws to Fix:\n{critique.critical_flaws}"}
        ]
        return await agenerate_structured(
            messages=messages, response_model=RefinedDraft,
            model=self.config.target_model, api_base=self.config.api_base, api_key=self.config.api_key
        )

    async def refine(self, task: TaskSpec, initial_draft: str, max_iterations: int = 2) -> str:
        logger.info(f"🛡️ [L4 Refine] Entering Adversarial Crucible (Max Iterations: {max_iterations})...")
        current_draft = initial_draft
        
        for i in range(max_iterations):
            critique = await self._critique(task, current_draft)
            if critique.passes_quality_bar and not critique.critical_flaws:
                logger.success("🛡️ [L4 Refine] Artifact passed quality threshold without flaws.")
                break
                
            logger.warning(f"🛡️ [L4 Refine] Flaws detected: {critique.critical_flaws}. Rewriting...")
            rewritten = await self._rewrite(current_draft, critique)
            current_draft = rewritten.improved_content
            
        return current_draft
