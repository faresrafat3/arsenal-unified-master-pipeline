"""ARSENAL DAG Orchestrator (State-Graph Architecture).

Replaces the bloated 'God Object' pipeline with a Composable Directed Acyclic Graph (DAG).
Inspired by LangGraph, this allows developers to snap L0-L6 layers together like LEGO blocks,
enabling infinite flexibility, pausing, resuming, and isolated testing.
"""
import asyncio
import networkx as nx
from typing import Dict, Any, Callable, Coroutine
from loguru import logger

from arsenal_ai.core.models import TaskSpec, ArsenalConfig, ArsenalResult
from arsenal_ai.layers.l0_router import TaxonomyRouter
from arsenal_ai.layers.l1_optimizer import InstructionOptimizer
from arsenal_ai.layers.l2_conductor import MetaConductor
from arsenal_ai.layers.l3_lats import LatsEngine
from arsenal_ai.layers.l4_refine import SelfRefineCrucible
from arsenal_ai.layers.l6_stages import AIScientistReviewer
from arsenal_ai.memory.voyager import VoyagerMemory, VoyagerSkill

class StateGraph:
    """A Lightweight SOTA State Graph Executor."""
    def __init__(self):
        self.graph = nx.DiGraph()
        self.entry_point = None

    def add_node(self, name: str, action: Callable):
        """Registers a cognitive node in the graph."""
        self.graph.add_node(name, action=action)

    def set_entry_point(self, name: str):
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str):
        """Defines the deterministic path between nodes."""
        self.graph.add_edge(from_node, to_node)
        
    def add_conditional_edges(self, from_node: str, condition: Callable[[Dict], str]):
        """Allows dynamic routing based on the state."""
        self.graph.nodes[from_node]['condition'] = condition

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the event loop traversing the graph."""
        current_node = self.entry_point
        
        while current_node:
            logger.debug(f"⚙️ [DAG Engine] Executing Node: {current_node}")
            node_data = self.graph.nodes[current_node]
            
            # Execute Node Action
            action = node_data['action']
            state = await action(state)
            
            # Determine next node
            if 'condition' in node_data:
                current_node = node_data['condition'](state)
            else:
                successors = list(self.graph.successors(current_node))
                current_node = successors[0] if successors else None
                
        return state

class ArsenalMasterPipeline:
    """Compiled DAG instance of the ARSENAL 10-System fusion."""
    
    def __init__(self, config: ArsenalConfig):
        self.config = config
        self.memory = VoyagerMemory()
        
        # Initialize instances
        self.router = TaxonomyRouter(config)
        self.optimizer = InstructionOptimizer(config)
        self.conductor = MetaConductor(config)
        self.lats = LatsEngine(config)
        self.refine = SelfRefineCrucible(config)
        self.scientist = AIScientistReviewer(config)
        
        self.dag = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Constructs the Neuro-Symbolic State Machine."""
        graph = StateGraph()
        
        # 1. Define Nodes (Wrappers to match state dict interface)
        async def node_memory(state: dict):
            skills = self.memory.retrieve_skills(state["task"].description)
            state["memory_context"] = "\n".join([s.executable_code for s in skills]) if skills else ""
            state["trace"].append(f"L5: Retrieved {len(skills)} skills")
            return state

        async def node_l0(state: dict):
            state["route"] = await self.router.route(state["task"])
            state["trace"].append("L0: Routing established")
            return state
            
        async def node_l1(state: dict):
            # Pass techniques properly
            opt = await self.optimizer.optimize(state["task"], state["route"].recommended_techniques)
            state["task"].description = opt.optimized_instruction
            state["trace"].append("L1: Instruction optimized")
            return state
            
        async def node_l2(state: dict):
            state["experts"] = await self.conductor.conduct(state["task"])
            state["best_thought"] = str(state["experts"])
            state["trace"].append("L2: Conductor execution")
            return state
            
        async def node_l3(state: dict):
            init_state = f"Task: {state['task'].description}\nExpert Insights: {str(state['experts'])[:500]}"
            state["best_thought"] = await self.lats.search(init_state, max_rollouts=2)
            state["trace"].append("L3: LATS Complete")
            return state
            
        async def node_l4(state: dict):
            state["best_thought"] = await self.refine.refine(state["task"], state["best_thought"])
            state["trace"].append("L4: Crucible Complete")
            return state
            
        async def node_l6(state: dict):
            review = await self.scientist.produce_artifact(state["task"], state["experts"], state["best_thought"])
            state["final_review"] = review
            state["trace"].append("L6: Artifact Crystallized")
            return state

        # Register Nodes
        graph.add_node("L5_Memory", node_memory)
        graph.add_node("L0_Router", node_l0)
        graph.add_node("L1_Optimizer", node_l1)
        graph.add_node("L2_Conductor", node_l2)
        graph.add_node("L3_LATS", node_l3)
        graph.add_node("L4_Crucible", node_l4)
        graph.add_node("L6_Review", node_l6)
        
        # Build DAG Edges
        graph.set_entry_point("L5_Memory")
        graph.add_edge("L5_Memory", "L0_Router")
        
        # Conditional Routing from L0
        def l0_router_condition(state: dict) -> str:
            if state["route"].recommended_techniques: return "L1_Optimizer"
            return "L2_Conductor"
        graph.add_conditional_edges("L0_Router", l0_router_condition)
        
        graph.add_edge("L1_Optimizer", "L2_Conductor")
        
        # Conditional Routing from L2
        def l2_router_condition(state: dict) -> str:
            if state["route"].activate_l3_search: return "L3_LATS"
            if state["route"].activate_l4_refine: return "L4_Crucible"
            return "L6_Review"
        graph.add_conditional_edges("L2_Conductor", l2_router_condition)
        
        graph.add_edge("L3_LATS", "L4_Crucible") # LATS flows into Refine
        graph.add_edge("L4_Crucible", "L6_Review")
        
        return graph

    async def execute(self, task: TaskSpec) -> ArsenalResult:
        logger.info(f"🚀 ARSENAL DAG IGNITED for Task: {task.task_id}")
        
        # Initial State
        state = {
            "task": task,
            "trace": [],
            "route": None,
            "experts": {},
            "best_thought": "",
            "final_review": None
        }
        
        # Execute the Graph
        final_state = await self.dag.execute(state)
        
        review = final_state["final_review"]
        
        # Post-Execution: Save back to memory
        if review and review.soundness_score > 0.8:
            self.memory.save_skill(VoyagerSkill(
                name=f"skill_{task.task_id}", 
                description=task.description, 
                executable_code=review.academic_summary
            ))
            
        logger.info("✅ ARSENAL DAG Execution Completed.")
        return ArsenalResult(
            task_id=task.task_id,
            final_artifact=review.academic_summary if review else "Error: Graph failed to reach L6",
            tokens_consumed=0,
            execution_trace=final_state["trace"],
            peer_review_score=review.soundness_score if review else 0.0
        )
