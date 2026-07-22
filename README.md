<div align="center">

# ⚙️ ARSENAL Unified Master Pipeline (v1.0.0-rc1)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen.svg?style=for-the-badge)](#)

**A**utomatic **R**easoning, **S**earch, **E**valuation, **N**avigation, and **A**daptive **L**earning

**An Executable, Asynchronous Neuro-Symbolic State Machine that unifies 10 state-of-the-art LLM agent frameworks into a single operational architecture.**

</div>

---

## 🌟 The 2026 SOTA Transformation

ARSENAL is no longer just a theoretical framework or a collection of prompts. It is a **fully executable Python package** powered by `LiteLLM`, `Instructor`, `ChromaDB`, and `AsyncIO`. It actively enforces determinism, runs python code in sandboxes, and dynamically routes LLM execution for maximum cognitive economy.

### 🔥 Architectural Highlights (L0 - L6)

- 🚦 **L0 Semantic Router:** Reads the user query and dynamically toggles heavy reasoning layers to prevent token waste (Cognitive Economy).
- 🛠️ **L1 Instruction Optimizer (OPRO):** Rewrites your prompt into a highly engineered Meta-Prompt with explicit guardrails against expected failure modes.
- 🎼 **L2 Meta-Conductor:** Dispatches specialized Expert Personas **concurrently**. Experts execute Python code in a native `Sandbox`, capture `stdout/stderr`, and self-correct via a ReAct loop.
- 🌳 **L3 Language Agent Tree Search (LATS):** True Monte Carlo Tree Search (MCTS) utilizing an LLM Process Reward Model (PRM) to evaluate, rollback, and optimize thought trajectories.
- 🛡️ **L4 Adversarial Crucible:** Self-Refine loops that ruthlessly critique drafts and force rewrites until they pass strict logical thresholds.
- 🧠 **L5 Voyager Memory:** Powered by `ChromaDB`, successful scripts and analytical frameworks are embedded and stored persistently. ARSENAL learns across sessions.
- 🎓 **L6 AI Scientist v2:** An automated peer-reviewer that grades the final artifact for academic soundness and actionability.

## 🏗️ The 10-System Fusion

We extracted the core logic, prompts, and flows from the top 10 LLM agent frameworks and unified them.

| # | Source System | How it's Executed in ARSENAL |
|---|---|---|
| 1 | **AI Scientist v2** | L6: Progressive peer review & write-up shell |
| 2 | **Self-Refine** | L4: Crucible rewrite loops based on critique |
| 3 | **Reflexion** | L5: Episodic failure tracing during MCTS rollouts |
| 4 | **Meta-Prompting** | L2: Asynchronous Conductor & Expert dispatch |
| 5 | **Tree of Thoughts** | L3: Beam/UCT search over framings |
| 6 | **LATS** | L3: PRM-evaluated rollouts and backpropagation |
| 7 | **APE / OPRO** | L1: Dynamic prompt optimization conditioned on context |
| 8 | **Voyager** | L5: ChromaDB persistent skill retrieval |
| 9 | **ReAct** | L2/Tools: Code execution, error observation, and correction |
| 10| **Prompt Report** | L0: Taxonomy-based architectural routing |

## 🚀 Getting Started

ARSENAL is designed to be imported as the reasoning engine for your downstream SaaS or Research platforms (e.g., `epistemic-forge`).

```bash
# 1. Install the package
pip install -e .

# 2. Run a full execution (Requires OPENAI_API_KEY or OPENROUTER_API_KEY)
export OPENAI_API_KEY="your-key-here"
```

```python
import asyncio
from arsenal_ai.core.models import ArsenalConfig, TaskSpec, Modality
from arsenal_ai.core.orchestrator import ArsenalMasterPipeline

async def run():
    config = ArsenalConfig(target_model="openai/gpt-4o-mini")
    pipeline = ArsenalMasterPipeline(config)
    
    task = TaskSpec(
        task_id="TASK_001",
        description="Write a Python script that calculates the 10th Fibonacci number in O(log n) time.",
        modality=Modality.CODE
    )
    
    result = await pipeline.execute(task)
    print(result.final_artifact)

asyncio.run(run())
```

## 📜 The Constitution
Universal, domain-agnostic prompts distilled from all extracted systems are injected globally via the `ConstitutionManager`. 
→ [`CONSTITUTION.md`](./CONSTITUTION.md)

---
<div align="center">
  <em>Built with care — from Cairo to the open web.</em>
</div>
