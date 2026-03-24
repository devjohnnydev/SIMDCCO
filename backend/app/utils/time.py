"""Timezone utilities for SIMDCCO"""
import pytz
from datetime import datetime
from ..config import settings

def get_current_time() -> datetime:
    """
    Get current time in configured system timezone (default: America/Sao_Paulo).
    Returns timezone-aware datetime.
    """
    tz = pytz.timezone(settings.TIMEZONE)
    return datetime.now(tz)

def to_system_time(dt: datetime) -> datetime:
    """
    Convert a datetime to system timezone.
    If naive, assumes UTC.
    """
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    
    tz = pytz.timezone(settings.TIMEZONE)
    return dt.astimezone(tz)
