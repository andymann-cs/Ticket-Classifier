import os
import requests

from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")


auth = HTTPBasicAuth(
    JIRA_EMAIL,
    JIRA_API_TOKEN
)

headers = {"Accept": "application/json"}

def get_issue(issue_key: str) -> dict:
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"

    response = requests.get(url, headers=headers, auth=auth, params={"fields": "summary, description, labels"})
    response.raise_for_status()

    return response.json()


def adf_to_text(node) -> str:
    if node is None:
        return ""

    if isinstance(node, list):
        return " ".join(
            adf_to_text(item)
            for item in node
        )

    if not isinstance(node, dict):
        return ""

    text = ""

    if node.get("type") == "text":
        text += node.get("text", "")

    if "content" in node:
        child_text = " ".join(
            adf_to_text(child)
            for child in node["content"]
        )

        if text and child_text:
            text += " "

        text += child_text

    return text.strip()


def add_label(issue_key: str, label: str):
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"

    response = requests.put(
        url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        json={
            "update": {
                "labels": [
                    {
                        "add": label
                    }
                ]
            }
        }
    )

    response.raise_for_status()





def get_ticket(issue_key: str) -> dict:
    issue = get_issue(issue_key)

    fields = issue["fields"]

    return {
        "key": issue["key"],
        "subject": fields.get("summary", ""),
        "description": adf_to_text(fields.get("description")),
        "labels": fields.get("labels", [])
    }




def add_comment(
    issue_key: str,
    category: str,
    confidence: float,
    route: str
):
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/comment"

    comment_text = (
        f"Automated ticket routing result\n\n"
        f"Predicted category: {category}\n"
        f"Confidence: {confidence:.2%}\n"
        f"Route: {route}"
    )

    body = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_text
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(
        url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        auth=auth,
        json=body
    )

    response.raise_for_status()

    return response.json()