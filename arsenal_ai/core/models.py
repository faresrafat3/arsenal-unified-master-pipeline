"""Core SOTA Data Models for ARSENAL Unified Master Pipeline.

Built using Pydantic to enforce Neuro-Symbolic structure and ensure 
all Agent communication is strictly typed and deterministic.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class Modality(str, Enum):
    TEXT = "text"
    CODE = "code"
    MATH = "math"

class ArsenalConfig(BaseModel):
    """Configuration for the Master Engine execution."""
    target_model: str = Field(default="openai/gpt-4o", description="Universal Hermes router string.")
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    max_budget_tokens: int = Field(default=50000, description="Hard token budget to prevent API bankruptcy.")
    enable_async_experts: bool = Field(default=True, description="Run L2 Conductor experts in parallel.")
    temperature: float = Field(default=0.0, description="Enforce determinism.")

class TaskSpec(BaseModel):
    """The unified input schema for any ARSENAL run."""
    task_id: str
    description: str
    modality: Modality
    constraints: List[str] = Field(default_factory=list)
    available_tools: List[str] = Field(default_factory=list)


class TaxonomyFamily(str, Enum):
    IN_CONTEXT = "In-Context Learning"
    ZERO_SHOT = "Zero-Shot"
    FEW_SHOT = "Few-Shot"
    THOUGHT_GEN = "Thought Generation"
    DECOMPOSITION = "Decomposition"

class L0RouteDecision(BaseModel):
    """L0 Prompt Report Taxonomy Router Output."""
    complexity_score: float = Field(ge=0.0, le=1.0, description="0.0 = Simple, 1.0 = Highly complex reasoning required.")
    recommended_families: List[TaxonomyFamily] = Field(description="Technique families from the Prompt Report to apply.")
    activate_l3_search: bool = Field(description="True if MCTS/Tree Search is needed.")
    activate_l4_refine: bool = Field(description="True if Adversarial Self-Refine is needed.")
    rationale: str = Field(description="Why this route was chosen.")

class L1OptimizedPrompt(BaseModel):
    """L1 OPRO/APE Optimizer Output."""
    optimized_instruction: str = Field(description="The heavily engineered meta-prompt to replace the user's raw query.")
    expected_failure_modes: List[str] = Field(description="Potential pitfalls downstream layers should watch out for.")

class ArsenalResult(BaseModel):
    """The final crystallized output of the pipeline."""
    task_id: str
    final_artifact: Any
    tokens_consumed: int
    execution_trace: List[Dict[str, Any]]
    peer_review_score: float
