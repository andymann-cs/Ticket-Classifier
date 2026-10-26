import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

from src.classifier import predict_ticket
from src.jira_client import get_ticket, add_label, add_comment
from src.router import choose_route
from typing import Optional

import logging

logger = logging.getLogger("ticket_router")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    "ticket_router.log",
    encoding="utf-8"
)

file_handler.setFormatter(
    logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
)

logger.addHandler(file_handler)
logger.info("Ticket router API started")

load_dotenv()

app = FastAPI()

WEBHOOK_SECRET = os.getenv("JIRA_WEBHOOK_SECRET")

class JiraWebhook(BaseModel):
    issue_key: str

@app.get("/")
def root():
    return {
        "status": "Ticket classifier API running"
    }

@app.post("/jira/webhook")
def jira_webhook(
    webhook: JiraWebhook,
    x_webhook_secret: Optional[str] = Header(default=None)
):
    logger.info(
        "Webhook received for issue=%s",
        webhook.issue_key
    )

    if x_webhook_secret != WEBHOOK_SECRET:
        logger.warning(
            "Rejected webhook for issue=%s: invalid or missing secret",
            webhook.issue_key
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid webhook secret"
        )

    issue_key = webhook.issue_key

    try:
        ticket = get_ticket(issue_key)

        prediction = predict_ticket(
            ticket["subject"],
            ticket["description"]
        )

        category = prediction["category"]
        confidence = prediction["confidence"]

        route = choose_route(
            category,
            confidence
        )

        add_label(issue_key, route)

        add_comment(
            issue_key,
            category,
            confidence,
            route
        )

        logger.info(
            "issue=%s category=%s confidence=%.4f route=%s",
            issue_key,
            category,
            confidence,
            route
        )

        return {
            "issue_key": issue_key,
            "category": category,
            "confidence": confidence,
            "route": route
        }

    except Exception:
        logger.exception(
            "Failed to process issue %s",
            issue_key
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to process Jira issue"
        )