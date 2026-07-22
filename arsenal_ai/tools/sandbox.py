"""Arsenal Native Tool Integrations (SOTA Agentic I/O)."""
from loguru import logger
import subprocess
import tempfile
import os

def execute_python_code(code: str, timeout: int = 5) -> str:
    """Safely executes a block of Python code and returns the stdout or traceback."""
    logger.info("🛠️ [Sandbox] Executing Python code block...")
    # In a true SOTA production environment, this should be executed in a Docker container or E2B sandbox.
    # For this master pipeline architecture, we execute it in an isolated subprocess.
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(code)
        temp_path = f.name
        
    try:
        result = subprocess.run(["python3", temp_path], capture_output=True, text=True, timeout=timeout)
        output = result.stdout if result.returncode == 0 else result.stderr
        return output[:2000] # Cap output length to prevent context bloat
    except subprocess.TimeoutExpired:
        return f"Error: Code execution exceeded {timeout} seconds."
    finally:
        os.remove(temp_path)

def search_web(query: str, max_results: int = 3) -> str:
    """Lightweight web search for live empirical data."""
    logger.info(f"🔍 [Sandbox] Searching web for: {query}")
    try:
        from duckduckgo_search import DDGS
        results = DDGS().text(query, max_results=max_results)
        return "\n".join([f"Source: {r.get('title')}\n{r.get('body')}" for r in results]) if results else "No results."
    except ImportError:
        return "Error: duckduckgo_search not installed."
    except Exception as e:
        return f"Search failed: {e}"
