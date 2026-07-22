"""ARSENAL Master Orchestrator (Neuro-Symbolic State Machine)."""
import asyncio
from loguru import logger
from arsenal_ai.core.models import TaskSpec, ArsenalConfig, ArsenalResult
from arsenal_ai.layers.l0_router import TaxonomyRouter
from arsenal_ai.layers.l1_optimizer import InstructionOptimizer
from arsenal_ai.domains.kaggle.mdp_agent import AutoKaggleMaster
from arsenal_ai.layers.l2_conductor import MetaConductor
from arsenal_ai.layers.l3_lats import LatsEngine
from arsenal_ai.layers.l4_refine import SelfRefineCrucible
from arsenal_ai.layers.l6_stages import AIScientistReviewer
from arsenal_ai.memory.voyager import VoyagerMemory, VoyagerSkill

class ArsenalMasterPipeline:
    def __init__(self, config: ArsenalConfig):
        self.config = config
        self.trace = []
        self.router = TaxonomyRouter(config)
        self.optimizer = InstructionOptimizer(config)
        self.conductor = MetaConductor(config)
        self.lats = LatsEngine(config)
        self.refine = SelfRefineCrucible(config)
        self.scientist = AIScientistReviewer(config)
        self.memory = VoyagerMemory()

    async def execute(self, task: TaskSpec) -> ArsenalResult:
        logger.info(f"🚀 ARSENAL IGNITED for Task: {task.task_id}")
        
        # DOMAIN SPECIFIC OVERRIDE (SOTA Specialized Agent Injection)
        if "kaggle" in task.description.lower() or "data science" in task.description.lower():
            logger.info("🧬 [Specialized Routing] Diverting to Autonomous Data Scientist (Kaggle MDP Mode).")
            # We initialize but for this architecture demonstration we just log it
            kaggle_agent = AutoKaggleMaster(self.config, max_iterations=3)
            self.trace.append({"layer": "Domain_Specialist", "action": "AutoKaggleMaster activated"})
        
        # L5: Voyager Memory
        skills = self.memory.retrieve_skills(task.description)
        skill_context = " ".join([s.executable_code for s in skills]) if skills else "No prior skills."
        self.trace.append({"layer": "L5", "action": f"Retrieved {len(skills)} skills"})
        
        # L0: Router
        route_decision = await self.router.route(task)
        self.trace.append({"layer": "L0", "action": "Routing established"})
        
        # L1: Optimizer
        optimized_instruction = await self.optimizer.optimize(task, route_decision.recommended_techniques)
        self.trace.append({"layer": "L1", "action": "Instruction optimized"})
        task.description = optimized_instruction.optimized_instruction
        
        # L2: Conductor
        expert_bundle = await self.conductor.conduct(task)
        self.trace.append({"layer": "L2", "action": "Experts dispatched and aggregated"})
        
        # L3 & L4
        best_thought = str(expert_bundle)
        if route_decision.activate_l3_search:
            initial_state = f"Task: {task.description}\nExpert Insights: {str(expert_bundle)[:500]}"
            best_thought = await self.lats.search(initial_state, max_rollouts=2)
            self.trace.append({"layer": "L3", "action": "LATS Search resolved"})
            
        refined_artifact = best_thought
        if route_decision.activate_l4_refine:
            refined_artifact = await self.refine.refine(task, best_thought)
            self.trace.append({"layer": "L4", "action": "Self-Refine complete"})
            
        # L6: Scientist Review
        review = await self.scientist.produce_artifact(task, expert_bundle, refined_artifact)
        self.trace.append({"layer": "L6", "action": f"Verdict: {review.final_decision}"})
        
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
            tokens_consumed=0,
            execution_trace=self.trace,
            peer_review_score=review.soundness_score
        )
