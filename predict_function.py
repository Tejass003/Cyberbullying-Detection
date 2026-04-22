from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
import torch
import torch.nn.functional as F
import numpy as np
import re, emoji

MODEL_PATH = "models/xlmr_cyberbully_model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer
tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL_PATH)
model = XLMRobertaForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

def clean_text(text):
    text = str(text).lower()
    text = emoji.demojize(text, delimiters=(" ", " "))
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"(.)\1{2,}", r"\1\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def predict_cyberbullying(text):
    cleaned_text = clean_text(text)

    inputs = tokenizer(
        cleaned_text,
        return_tensors="pt",
        max_length=128,
        padding="max_length",
        truncation=True
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = F.softmax(logits, dim=1).cpu().numpy()[0]

    predicted_class_id = np.argmax(probabilities)
    labels = {0: "NON-CYBERBULLYING", 1: "CYBERBULLYING"}
    predicted_label = labels[predicted_class_id]
    confidence = probabilities[predicted_class_id] * 100
    bully_prob = probabilities[1] * 100

    return predicted_label, confidence, bully_prob
