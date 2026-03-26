from fastapi import Request
from datetime import datetime
from app.db import insert, get

def log_event(email_id, event_type, request: Request):
    insert("events", {
        "email_id": email_id,
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent")
    })

def get_original_url(tracking_id):
    result = get("links", f"tracking_id=eq.{tracking_id}")
    return result[0] if result else None