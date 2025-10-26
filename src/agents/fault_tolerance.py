# src/agents/fault_tolerance.py
import asyncio
import logging
from agno import RetryPolicy

log = logging.getLogger(__name__)

# -------------------------------
# TODO2: Session 3 - Fault Tolerance / Retry Skeleton
# -------------------------------
# Students will implement retry logic for multi-agent workflows
# Reference: Notebook Cells 4-5

async def retry_task_with_feedback(
    coro_func,
    *args,
    retry_policy: RetryPolicy = None,
    feedback_condition=None,
    **kwargs
):
    """
    Wraps any coroutine function (e.g., agent.handle) with retry and optional feedback.
    
    Args:
        coro_func: coroutine function to run (e.g., CrewAgentWrapper.handle)
        *args, **kwargs: arguments to pass to coro_func
        retry_policy: Agno RetryPolicy object (optional)
        feedback_condition: async callable(task_result) -> bool, triggers retry if True

    Returns:
        result: final output of the coroutine after retries
    """

    # -------------------------------
    # Skeleton: Students must implement
    # -------------------------------
    # 1) Determine max_attempts and backoff from retry_policy
    max_attempts = retry_policy.max_attempts if retry_policy else 1
    backoff = getattr(retry_policy, "backoff_factor", 1) if retry_policy else 1

    # 2) Attempt loop
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        try:
            log.info("Attempt %d/%d for %s", attempt, max_attempts, coro_func.__name__)

            # TODO: Call the coroutine function with args/kwargs
            # Example:
            # result = await coro_func(*args, **kwargs)
            result = None  # <- students replace with actual call

            # -------------------------------
            # TODO: Apply feedback condition
            # If feedback_condition(result) returns True, retry
            # -------------------------------
            if feedback_condition:
                retry_needed = await feedback_condition(result)
                if retry_needed:
                    log.warning("Feedback triggered retry for attempt %d", attempt)
                    await asyncio.sleep(backoff * attempt)
                    continue

            # Success path
            return result

        except Exception as e:
            log.exception("Error in attempt %d: %s", attempt, e)
            if attempt < max_attempts:
                log.info("Retrying after backoff: %ds", backoff * attempt)
                await asyncio.sleep(backoff * attempt)
            else:
                log.error("Max retries reached for %s", coro_func.__name__)
                # Optional: return error dict instead of raising
                return {"status": "failed", "error": str(e)}

    # Fallback
    log.error("Task failed after %d attempts: %s", max_attempts, coro_func.__name__)
    return None
