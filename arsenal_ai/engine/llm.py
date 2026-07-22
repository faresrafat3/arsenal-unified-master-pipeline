"""Asynchronous Hermes-Style LLM Engine.

Supports 100+ providers via LiteLLM + Instructor, optimized for 
parallel execution in the L2 and L3 layers.
"""
from pydantic import BaseModel
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
import instructor
from litellm import acompletion

try:
    # Use Async LiteLLM for true parallel multi-agent execution
    client = instructor.from_litellm(acompletion)
except Exception as e:
    logger.warning(f"LiteLLM Async initialization failed: {e}")
    client = None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def agenerate_structured(
    messages: list, 
    response_model: type[BaseModel], 
    model: str, 
    temperature: float = 0.0,
    api_base: str = None,
    api_key: str = None
) -> BaseModel:
    """SOTA Async Structured Extraction."""
    if not client:
        raise ValueError("Universal LLM Async Router not initialized.")
        
    try:
        logger.debug(f"🌐 [Async Hermes] Dispatching to [{model}] for schema [{response_model.__name__}]...")
        call_params = {
            "model": model,
            "messages": messages,
            "response_model": response_model,
            "temperature": temperature,
        }
        if api_base: call_params["api_base"] = api_base
        if api_key: call_params["api_key"] = api_key
            
        return await client.chat.completions.create(**call_params)
    except Exception as e:
        logger.error(f"🌐 [Async Hermes] Failure: {e}")
        raise
