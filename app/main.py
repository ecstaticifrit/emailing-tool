from fastapi import FastAPI, Request
from fastapi.responses import Response, RedirectResponse
import uuid
from app.email_sender import send_email
from app.utils import process_email_html
from app.db import insert
from app.tracker import log_event, get_original_url

app = FastAPI()

# -------------------------------
# SEND EMAIL
# -------------------------------
@app.post("/send-email")
async def send_email_api(payload: dict, request: Request):
    email_id = str(uuid.uuid4())

    base_url = str(request.base_url).rstrip("/")
    html = process_email_html(payload["body"], email_id, base_url)

    insert("emails", {
        "id": email_id,
        "to_email": payload["to"],
        "subject": payload["subject"],
        "body": html,
        "status": "sent"
    })

    send_email(payload["to"], payload["subject"], html)

    return {"message": "Email sent", "email_id": email_id}


# -------------------------------
# TRACK OPEN
# -------------------------------
@app.get("/track/open/{email_id}")
async def track_open(email_id: str, request: Request):
    log_event(email_id, "open", request)

    pixel = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
    return Response(content=pixel, media_type="image/gif")


# -------------------------------
# TRACK CLICK
# -------------------------------
@app.get("/track/click/{tracking_id}")
async def track_click(tracking_id: str, request: Request):
    link = get_original_url(tracking_id)

    if not link:
        return {"error": "Invalid link"}

    log_event(link["email_id"], "click", request)

    return RedirectResponse(link["original_url"])