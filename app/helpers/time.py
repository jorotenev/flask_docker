from datetime import datetime, timezone


def utc_now_str():
    return datetime.now(timezone.utc).isoformat()
