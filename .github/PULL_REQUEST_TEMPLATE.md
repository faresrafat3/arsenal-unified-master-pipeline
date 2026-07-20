## Objective
<!-- Describe the specific goal of this PR. Which LLM framework or logic flow are you updating/fixing? -->

## Pipeline Impact (Check the affected layers)
- [ ] **L0:** Prompt Report Taxonomy Router
- [ ] **L1:** Instruction Optimizer (APE / OPRO)
- [ ] **L2:** Meta-Prompting Conductor
- [ ] **L3:** Tree Search (ToT / LATS)
- [ ] **L4:** Self-Refine Loop
- [ ] **L5:** Episodic Memory (Reflexion / Voyager)
- [ ] **L6:** Writeup/Evaluation Wrap-up (AI Scientist)

## Prompt Engineering Checklist
<!-- If you modified prompts, check the following: -->
- [ ] Did you abstract the prompt instead of hardcoding it?
- [ ] Is `CONSTITUTION.md` updated if this adds a universal rule?
- [ ] Have you tested for prompt injection or context-window bloat?

## Architectural Integrity
- [ ] I have updated the `python_logic_inventory.json` if I added new functions.
- [ ] I have updated the Mermaid graphs (`graphs/`) to reflect any routing changes.
- [ ] This change maintains the modularity of the pipeline (does not create a monolith).
