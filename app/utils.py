import uuid
from bs4 import BeautifulSoup
from app.config import BASE_URL
from app.db import insert

def process_email_html(html, email_id):
    soup = BeautifulSoup(html, "html.parser")

    # Replace links
    for a in soup.find_all("a", href=True):
        original_url = a["href"]
        tracking_id = str(uuid.uuid4())

        insert("links", {
            "email_id": email_id,
            "original_url": original_url,
            "tracking_id": tracking_id
        })

        a["href"] = f"{BASE_URL}/track/click/{tracking_id}"

    # Add tracking pixel
    pixel = soup.new_tag(
        "img",
        src=f"{BASE_URL}/track/open/{email_id}",
        width="1",
        height="1"
    )
    soup.append(pixel)

    return str(soup)