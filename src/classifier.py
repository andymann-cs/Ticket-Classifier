import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

MODEL_PATH = "models/weighted_distilbert"

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_PATH
)

model.to(device)
model.eval()


def predict_ticket(subject: str, description: str):
    text = f"{subject} {description}"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=1)

    confidence, predicted_id = torch.max(
        probabilities,
        dim=1
    )

    predicted_id = predicted_id.item()
    confidence = confidence.item()

    category = model.config.id2label[predicted_id]

    return {
        "category": category,
        "confidence": confidence
    }