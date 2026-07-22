"""L6: AI Scientist v2 Progressive Stage Shell.

Provides the ultimate academic wrap-up. It takes the messy outputs from 
L2 (Conductor) and L3 (LATS Search) and synthesizes them into a polished, 
peer-reviewed academic artifact, issuing a final 'Accept/Reject' verdict.
"""
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from loguru import logger
from arsenal_ai.engine.llm import agenerate_structured
from arsenal_ai.core.models import ArsenalConfig, TaskSpec

class PeerReviewVerdict(BaseModel):
    clarity_score: float = Field(ge=0.0, le=1.0)
    soundness_score: float = Field(ge=0.0, le=1.0)
    final_decision: str = Field(description="Accept, Minor Revisions, Major Revisions, or Reject.")
    academic_summary: str = Field(description="The crystallized, publish-ready writeup of the entire process.")

class AIScientistReviewer:
    def __init__(self, config: ArsenalConfig):
        self.config = config

    async def produce_artifact(self, task: TaskSpec, raw_evidence: Dict[str, Any], best_thought: str) -> PeerReviewVerdict:
        logger.info("🎓 [L6 AI Scientist] Commencing final peer review and crystallization...")
        
        messages = [
            {"role": "system", "content": "You are the L6 AI Scientist Reviewer (NeurIPS level). Take the raw evidence and search results from the agents below, synthesize them into a flawless academic summary, and grade the soundness of the research."},
            {"role": "user", "content": f"Task: {task.description}\n\nEvidence Bundle: {raw_evidence}\n\nLATS Best Thought: {best_thought}"}
        ]
        
        result: PeerReviewVerdict = await agenerate_structured(
            messages=messages,
            response_model=PeerReviewVerdict,
            model=self.config.target_model,
            api_base=self.config.api_base,
            api_key=self.config.api_key
        )
        
        logger.success(f"🎓 [L6 AI Scientist] Verdict Issued: {result.final_decision} (Soundness: {result.soundness_score})")
        return result
