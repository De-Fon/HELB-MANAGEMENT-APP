import random
import string
from datetime import datetime, timezone

def generate_random_string(length: int = 10) -> str:
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def get_current_utc_time() -> datetime:
    """Return the current time strictly in UTC timezone."""
    return datetime.now(timezone.utc)

def paginate(items: list, page: int, size: int, total: int) -> dict:
    """
    Format a standard pagination response.
    Can be used by any route returning lists of items.
    """
    return {
        "data": items,
        "meta": {
            "total": total,
            "page": page,
            "size": size,
            "has_next": (page * size) < total,
            "has_previous": page > 1
        }
    }
