"""L5: Episodic Memory (Reflexion).

Maintains a short-term trajectory of failures and verbal self-reflections 
during a single run to prevent the agent from repeating the same mistakes 
in L3/L4 loops.
"""
from typing import List
from pydantic import BaseModel, Field

class Reflection(BaseModel):
    failed_action: str = Field(description="The action that failed.")
    critique: str = Field(description="Why it failed.")
    lesson: str = Field(description="Verbal instruction on what to do differently next time.")

class ReflexionMemory:
    def __init__(self):
        self.reflections: List[Reflection] = []
        
    def add_reflection(self, reflection: Reflection):
        self.reflections.append(reflection)
        
    def get_context(self) -> str:
        if not self.reflections:
            return ""
        context = "PAST FAILURES TO AVOID:\\n"
        for i, r in enumerate(self.reflections):
            context += f"{i+1}. Tried: {r.failed_action}\\n   Failed because: {r.critique}\\n   Lesson: {r.lesson}\\n"
        return context
