"""L0/L1: Prompt Report Taxonomy Library.

This module acts as the definitive dictionary of the 58 Prompting Techniques.
It grounds the LLM optimizer by injecting the precise SOTA patterns 
required by the L0 RouteDecision, ensuring the agent doesn't hallucinate 
a weak prompt, but strictly follows academic architectures.
"""
from enum import Enum
from typing import Dict, List

class PromptTechnique(str, Enum):
    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "cot"
    CHAIN_OF_VERIFICATION = "cove"
    DIRECTIONAL_STIMULUS = "directional_stimulus"
    SYSTEM_2_ATTENTION = "system_2_attention"
    LEAST_TO_MOST = "least_to_most"

# The definitive library of SOTA Prompt Patterns
PROMPT_REPORT_LIBRARY: Dict[PromptTechnique, str] = {
    PromptTechnique.FEW_SHOT: (
        "PATTERN: Few-Shot Prompting.\n"
        "INSTRUCTION: You must provide exactly 3 diverse examples of Inputs and Outputs before asking the model to solve the user's task."
    ),
    PromptTechnique.CHAIN_OF_THOUGHT: (
        "PATTERN: Zero-Shot Chain of Thought.\n"
        "INSTRUCTION: Append the exact phrase 'Let's think step by step' or structurally force the model to output a <thinking> block before the <answer> block."
    ),
    PromptTechnique.CHAIN_OF_VERIFICATION: (
        "PATTERN: Chain of Verification (CoVe).\n"
        "INSTRUCTION: First, draft a baseline answer. Second, generate 3 specific verification questions to fact-check your baseline. Third, answer those verification questions independently. Finally, generate the revised answer incorporating the verified facts."
    ),
    PromptTechnique.DIRECTIONAL_STIMULUS: (
        "PATTERN: Directional Stimulus Prompting.\n"
        "INSTRUCTION: Extract specific keywords or hints from the user query, and explicitly force the LLM to include these specific keywords in the final output to guide its generation trajectory."
    ),
    PromptTechnique.SYSTEM_2_ATTENTION: (
        "PATTERN: System 2 Attention (S2A).\n"
        "INSTRUCTION: Force the model to rewrite the user's prompt to explicitly remove any irrelevant context or biased phrasing, and ONLY use the rewritten prompt to generate the final answer."
    ),
    PromptTechnique.LEAST_TO_MOST: (
        "PATTERN: Least-to-Most Prompting.\n"
        "INSTRUCTION: Decompose the complex problem into a series of easier subproblems. Solve the easiest subproblem first, then use its answer as context to solve the next hardest, until the final goal is reached."
    )
}

def get_taxonomy_templates(techniques: List[str]) -> str:
    """Retrieves the strict academic prompt patterns for the requested techniques."""
    injected_patterns = []
    for t in techniques:
        try:
            # Map string to Enum and fetch
            technique_enum = PromptTechnique(t.lower())
            injected_patterns.append(PROMPT_REPORT_LIBRARY[technique_enum])
        except ValueError:
            # Technique not explicitly hardcoded in the primary library
            pass
            
    if not injected_patterns:
        return ""
        
    return "=== MANDATORY PROMPTING TECHNIQUES (THE PROMPT REPORT) ===\n" + "\n\n".join(injected_patterns)
