# Contributing to ARSENAL

First off, thank you for considering contributing to the **ARSENAL Unified Master Pipeline**. 
Because this repository represents a highly intricate fusion of 10 different LLM agent frameworks (from APE and OPRO to LATS and AI Scientist v2), contributions must follow strict architectural guidelines to ensure we don't break the cognitive flow.

## 🏗️ Architectural Guidelines for Contributions

When modifying the pipeline, you must identify which layer (L0-L6) your PR affects:
1. **L0 (Router):** Prompt Report Taxonomy.
2. **L1 (Optimizer):** APE / OPRO instruction tuning.
3. **L2 (Conductor):** Meta-Prompting expert dispatch.
4. **L3 (Search/Reasoning):** ToT / LATS node expansions.
5. **L4 (Refinement):** Self-Refine loops.
6. **L5 (Memory):** Reflexion / Voyager skill saving.
7. **L6 (Staging):** AI Scientist v2 progressive evaluation.

### Modifying Prompts
If your contribution modifies core prompts:
- You **must** update `prompts_complete.md`.
- Ensure any domain-agnostic principles are synced with `CONSTITUTION.md`.
- Avoid hardcoding system prompts inside Python logic; they should be abstracted and imported.

### Modifying Logic & Routing
If you are adding a new technique (e.g., integrating a new paper's logic):
- Update `python_logic_inventory.json` with the new functional footprint.
- Ensure the Mermaid graphs (`graphs/MASTER_UNIFIED_ENGLISH.mmd`) accurately reflect the new path.

## 🧪 Testing Your Changes
Before submitting a PR, ensure that:
1. The **Conductor** can successfully dispatch your new tool/expert.
2. Token usage hasn't exponentially bloated (we are building cost-aware AI).
3. The Fallback mechanics are intact.

Please refer to the detailed Pull Request template when submitting your code.
