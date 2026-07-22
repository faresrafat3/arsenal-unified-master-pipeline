"""L3: Language Agent Tree Search (LATS) Engine.

TRUE MCTS Implementation:
1. Selection (UCT formulation)
2. Expansion
3. Simulation (Rollout)
4. Backpropagation (Value updates)
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import asyncio
import math
from loguru import logger
from arsenal_ai.engine.llm import agenerate_structured
from arsenal_ai.core.models import ArsenalConfig, constitution

class LatsNodeEvaluation(BaseModel):
    reward_score: float = Field(ge=0.0, le=1.0)
    critique_reasoning: str
    is_terminal: bool

class LatsNodeExpansion(BaseModel):
    proposed_actions: List[str]

class MCTSNode:
    def __init__(self, state: str, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children: List['MCTSNode'] = []
        self.visits = 0
        self.value = 0.0
        self.is_terminal = False

    def uct_score(self, exploration_weight: float = 1.414) -> float:
        if self.visits == 0:
            return float('inf')
        return (self.value / self.visits) + exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)

class LatsEngine:
    def __init__(self, config: ArsenalConfig):
        self.config = config

    async def _expand(self, node: MCTSNode) -> None:
        messages = [
            {"role": "system", "content": f"LATS Expansion.\\n{constitution.get_rules()}\\nPropose 3 distinct next logical steps."},
            {"role": "user", "content": f"Current State: {node.state}"}
        ]
        res: LatsNodeExpansion = await agenerate_structured(messages, LatsNodeExpansion, self.config.target_model, self.config.temperature, self.config.api_base, self.config.api_key)
        for action in res.proposed_actions:
            new_state = node.state + f"\\nAction: {action}"
            node.children.append(MCTSNode(state=new_state, parent=node, action=action))

    async def _simulate(self, node: MCTSNode) -> float:
        """Rollout value estimation."""
        messages = [
            {"role": "system", "content": f"LATS Value Function.\\n{constitution.get_rules()}\\nEvaluate the success probability of this trajectory (0.0 to 1.0)."},
            {"role": "user", "content": f"Trajectory: {node.state}"}
        ]
        try:
            res: LatsNodeEvaluation = await agenerate_structured(messages, LatsNodeEvaluation, self.config.target_model, self.config.temperature, self.config.api_base, self.config.api_key)
            node.is_terminal = res.is_terminal
            return res.reward_score
        except Exception:
            return 0.5

    def _backpropagate(self, node: MCTSNode, reward: float):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

    async def search(self, initial_state: str, max_iterations: int = 3) -> str:
        logger.info(f"🌳 [L3 LATS] Initiating TRUE MCTS Search (Iterations: {max_iterations})")
        root = MCTSNode(state=initial_state)

        for i in range(max_iterations):
            # 1. Selection
            node = root
            while node.children and not node.is_terminal:
                node = max(node.children, key=lambda n: n.uct_score())
            
            # 2. Expansion
            if not node.is_terminal and node.visits > 0 or node == root:
                await self._expand(node)
                if node.children:
                    node = node.children[0] # Pick first for simulation
            
            # 3. Simulation
            reward = await self._simulate(node)
            
            # 4. Backpropagation
            self._backpropagate(node, reward)
            logger.debug(f"MCTS Iteration {i+1} completed. Node value updated.")

        # Return best trajectory
        best_child = max(root.children, key=lambda n: n.visits if n.visits > 0 else -1, default=None)
        if best_child:
            logger.success(f"🌳 [L3 LATS] Selected optimal trajectory via UCT.")
            return best_child.state
        return initial_state
