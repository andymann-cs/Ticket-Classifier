import sys

from src.classifier import predict_ticket
from src.jira_client import get_ticket, add_label
from src.router import ROUTES, CONFIDENCE_THRESHOLD


def main():
    issue_key = sys.argv[1]

    ticket = get_ticket(issue_key)

    prediction = predict_ticket(
        ticket["subject"],
        ticket["description"]
    )

    category = prediction["category"]
    confidence = prediction["confidence"]

    print(f"\nTicket: {ticket['key']}")
    print(f"Prediction: {category}")
    print(f"Confidence: {confidence:.2%}")

    if confidence >= CONFIDENCE_THRESHOLD:
        route = ROUTES[category]

        add_label(issue_key, route)

        print(f"Routed to: {route}")
    else:
        add_label(issue_key, "manual-review")

        print("Low confidence — sent for manual review")


if __name__ == "__main__":
    main()