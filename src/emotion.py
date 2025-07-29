from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from torch.nn.functional import softmax

tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")

emotion_to_emojis = {
    "joy": ["😊", "😄", "😆"],
    "sadness": ["😞", "😢", "😭"],
    "anger": ["😡", "😠", "😤"],
    "fear": ["😨", "😰", "😱"],
    "surprise": ["😲", "😳", "😮"],
    "disgust": ["🤢", "🤮", "😒"],
    "neutral": ["😐", "😶", "😑"]
}

def get_emotion_and_score(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"])
    probs = softmax(outputs.logits, dim=1)[0]
    predicted_idx = probs.argmax().item()
    label = model.config.id2label[predicted_idx]
    score = probs[predicted_idx].item()
    return label, score

def choose_emoji(emotion, score, guild_id=None, client=None):
    if guild_id is not None and client and hasattr(client, "guild_emoji_settings"):
        guild_emojis = client.guild_emoji_settings.get(str(guild_id), {})
        emojis = guild_emojis.get(emotion, emotion_to_emojis.get(emotion, ["❓"]))
    else:
        emojis = emotion_to_emojis.get(emotion, ["❓"])

    if score < 0.6:
        idx = 0
    elif score < 0.85:
        idx = 1
    else:
        idx = 2

    return emojis[idx]
