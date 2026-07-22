"""SOTA Secure Python Sandbox (E2B Cloud Code Interpreter).

Replaces the dangerous local `subprocess` with a fully isolated, 
production-grade cloud container. The AI can now safely install packages, 
run complex logic, and interact with a virtual filesystem without 
risking the host machine.
"""
import os
from loguru import logger
from typing import Dict, Any

try:
    from e2b_code_interpreter import Sandbox
    E2B_AVAILABLE = True
except ImportError:
    E2B_AVAILABLE = False

class CodeSandbox:
    @staticmethod
    def execute(code: str, timeout: int = 30) -> Dict[str, Any]:
        """Safely executes Python code in a stateful cloud sandbox."""
        logger.info("🛠️ [Sandbox] Requesting secure execution environment...")
        
        e2b_key = os.environ.get("E2B_API_KEY")
        
        if E2B_AVAILABLE and e2b_key:
            logger.debug("🔒 [Sandbox] Provisioning E2B Secure Cloud Container...")
            try:
                # E2B Provisions a remote isolated Linux container in milliseconds
                with Sandbox(api_key=e2b_key) as sandbox:
                    execution = sandbox.run_code(code, timeout=timeout)
                    
                    output = ""
                    if execution.logs.stdout:
                        output += "\n".join(execution.logs.stdout)
                    if execution.results:
                        for res in execution.results:
                            if res.text: output += res.text
                            
                    error = "\n".join(execution.logs.stderr) if execution.logs.stderr else ""
                    if execution.error:
                        error += f"\n{execution.error.name}: {execution.error.value}"
                        
                    success = not bool(execution.error) and not bool(execution.logs.stderr)
                    
                    return {
                        "success": success,
                        "output": output[:2000], # Prevent context window bloat
                        "error": error[:2000]
                    }
            except Exception as e:
                logger.error(f"E2B Cloud Execution failed: {e}")
                return {"success": False, "output": "", "error": f"Sandbox crash: {e}"}
        else:
            # Dangerous Fallback for local testing only
            logger.warning("⚠️ [SECURITY ALERT] E2B_API_KEY missing. Falling back to UNSAFE local subprocess execution. DO NOT USE IN PRODUCTION.")
            import subprocess, tempfile
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(code)
                temp_path = f.name
            try:
                res = subprocess.run(["python3", temp_path], capture_output=True, text=True, timeout=timeout)
                success = res.returncode == 0
                return {
                    "success": success,
                    "output": res.stdout[:2000],
                    "error": res.stderr[:2000] if not success else ""
                }
            except Exception as e:
                return {"success": False, "output": "", "error": str(e)}
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
