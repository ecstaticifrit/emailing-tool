import requests
from app.config import SUPABASE_URL, SUPABASE_KEY

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def insert(table, data):
    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/{table}",
        headers=HEADERS,
        json=data
    )

    # Debug logging (VERY IMPORTANT)
    print("STATUS:", res.status_code)
    print("RESPONSE:", res.text)

    if res.status_code >= 400:
        raise Exception(f"Supabase Error: {res.text}")

    # Handle empty response safely
    if not res.text:
        return {}

    return res.json()

def get(table, filters=""):
    res = requests.get(f"{SUPABASE_URL}/rest/v1/{table}?{filters}", headers=HEADERS)
    return res.json()