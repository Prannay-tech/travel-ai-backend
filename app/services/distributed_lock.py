import asyncio
import logging
from contextlib import asynccontextmanager
from app.core.config import settings
import redis.asyncio as redis

logger = logging.getLogger(__name__)

# Global Redis Pool for the backend
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class DistributedLockError(Exception):
    pass

@asynccontextmanager
async def transactional_lock(lock_key: str, timeout_seconds: int = 30):
    """
    Prevents double-booking and accidental double-charges.
    Acquires a distributed lock in Redis for the specific transaction.
    If the lock is already held (e.g. user clicked 'Book' twice really fast),
    it raises a DistributedLockError to abort the second transaction.
    """
    full_key = f"lock:transaction:{lock_key}"
    
    # Attempt to acquire lock. NX=True ensures it only sets if it doesn't exist.
    # EX=timeout_seconds ensures the lock auto-expires if the server crashes, 
    # preventing permanent deadlocks.
    acquired = await redis_client.set(full_key, "locked", nx=True, ex=timeout_seconds)
    
    if not acquired:
        logger.warning(f"CRITICAL: Transaction lock collision detected on {full_key}")
        raise DistributedLockError("Transaction is already in progress. Please wait.")
        
    try:
        # Yield control back to the booking orchestrator
        yield
    finally:
        # Guarantee the lock is released when the transaction finishes (or fails)
        await redis_client.delete(full_key)
