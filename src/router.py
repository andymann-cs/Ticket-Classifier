ROUTES = {
    "Account": "account-support",
    "Communication": "communications-support",
    "Hardware": "hardware-support",
    "Network": "network-support",
    "RemoteWork": "remote-work-support",
    "Security": "security-support",
    "Software": "software-support",
    "Training": "training-support",
}

CONFIDENCE_THRESHOLD = 0.70

def choose_route(category: str, confidence: float) -> str:
    if confidence < CONFIDENCE_THRESHOLD:
        return "manual-review"

    return ROUTES[category]
