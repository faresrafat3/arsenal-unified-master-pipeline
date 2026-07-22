"""L5: Procedural Skill Memory (Voyager-style).

Uses ChromaDB to persistently store successful code/logic blocks.
When ARSENAL encounters a novel task, it searches this vector store 
to automatically retrieve and utilize previously mastered skills.
"""
from typing import List, Optional
import chromadb
from loguru import logger
from pydantic import BaseModel, Field

class VoyagerSkill(BaseModel):
    name: str = Field(description="Name of the skill (e.g., 'data_cleaner_v1').")
    description: str = Field(description="Semantic description of what the code/logic does.")
    executable_code: str = Field(description="The actual code or logic block.")

class VoyagerMemory:
    def __init__(self, persist_dir: str = ".arsenal_voyager_db"):
        try:
            self.client = chromadb.PersistentClient(path=persist_dir)
            self.collection = self.client.get_or_create_collection(name="voyager_skills")
            logger.info("🧠 [L5 Voyager] Persistent Vector Skill Library Initialized.")
        except Exception as e:
            logger.warning(f"ChromaDB failed: {e}. Using ephemeral memory.")
            self.client = chromadb.Client()
            self.collection = self.client.create_collection(name="voyager_skills")

    def save_skill(self, skill: VoyagerSkill):
        """Commits a successfully verified skill to long-term memory."""
        try:
            self.collection.add(
                documents=[skill.description],
                metadatas=[{"code": skill.executable_code, "name": skill.name}],
                ids=[skill.name]
            )
            logger.success(f"🧠 [L5 Voyager] Skill '{skill.name}' crystallized in memory.")
        except Exception as e:
            logger.error(f"Failed to save skill: {e}")

    def retrieve_skills(self, task_description: str, top_k: int = 2) -> List[VoyagerSkill]:
        """Auto-retrieves contextually relevant skills to bootstrap the current task."""
        try:
            if self.collection.count() == 0:
                return []
                
            results = self.collection.query(
                query_texts=[task_description],
                n_results=min(top_k, self.collection.count())
            )
            
            skills = []
            if results and 'metadatas' in results and results['metadatas'][0]:
                for meta in results['metadatas'][0]:
                    skills.append(VoyagerSkill(
                        name=meta.get("name", "unknown"),
                        description="", # Restored if needed
                        executable_code=meta.get("code", "")
                    ))
            logger.debug(f"🧠 [L5 Voyager] Retrieved {len(skills)} relevant skills.")
            return skills
        except Exception as e:
            logger.warning(f"Voyager Retrieval Failed: {e}")
            return []
