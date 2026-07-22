"""ARSENAL Master Orchestrator (Neuro-Symbolic State Machine)."""
import asyncio
from loguru import logger
from arsenal_ai.core.models import TaskSpec, ArsenalConfig, ArsenalResult
from arsenal_ai.layers.l2_conductor import MetaConductor
from arsenal_ai.layers.l3_lats import LatsEngine
from arsenal_ai.layers.l6_stages import AIScientistReviewer
from arsenal_ai.memory.voyager import VoyagerMemory, VoyagerSkill

class ArsenalMasterPipeline:
    """The central Nervous System of ARSENAL."""
    
    def __init__(self, config: ArsenalConfig):
        self.config = config
        self.trace = []
        self.conductor = MetaConductor(config)
        self.lats = LatsEngine(config)
        self.scientist = AIScientistReviewer(config)
        self.memory = VoyagerMemory()

    async def execute(self, task: TaskSpec) -> ArsenalResult:
        """Runs the fully integrated SOTA pipeline."""
        logger.info(f"🚀 ARSENAL IGNITED for Task: {task.task_id}")
        
        # 1. Voyager Memory (Retrieve prior skills)
        skills = self.memory.retrieve_skills(task.description)
        skill_context = "\n".join([s.executable_code for s in skills]) if skills else "No prior skills."
        self.trace.append({"layer": "L5", "action": f"Retrieved {len(skills)} skills"})
        
        # 2. Conductor (Meta-Prompting / Dispatch)
        expert_bundle = await self.conductor.conduct(task)
        self.trace.append({"layer": "L2", "action": "Experts dispatched and aggregated"})
        
        # 3. LATS Search (Deep Reasoning)
        initial_state = f"Task: {task.description}\nExpert Insights: {str(expert_bundle)[:500]}"
        best_thought = await self.lats.search(initial_state, max_rollouts=3)
        self.trace.append({"layer": "L3", "action": "LATS Search resolved"})
        
        # 4. AI Scientist Review (Crystallization)
        review = await self.scientist.produce_artifact(task, expert_bundle, best_thought)
        self.trace.append({"layer": "L6", "action": f"Verdict: {review.final_decision}"})
        
        # Optionally save new skills to Voyager
        if review.soundness_score > 0.8:
            self.memory.save_skill(VoyagerSkill(
                name=f"skill_{task.task_id}", 
                description=task.description, 
                executable_code=review.academic_summary
            ))
        
        logger.info("✅ ARSENAL Pipeline Execution Completed Successfully.")
        return ArsenalResult(
            task_id=task.task_id,
            final_artifact=review.academic_summary,
            tokens_consumed=0, # In a full prod version, hook this to litellm cost tracking
            execution_trace=self.trace,
            peer_review_score=review.soundness_score
        )
