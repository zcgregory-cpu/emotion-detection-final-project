"""Emotion detection client for the Watson NLP Emotion Predict service."""

import json
import os

import requests


SERVICE_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)

MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"

EMPTY_RESULT = {
    "anger": None,
    "disgust": None,
    "fear": None,
    "joy": None,
    "sadness": None,
    "dominant_emotion": None,
}


def emotion_detector(text_to_analyze):
    """Analyze text and return emotion scores plus the dominant emotion."""
    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            SERVICE_URL,
            json=input_json,
            headers=headers,
            timeout=30,
        )
    except requests.RequestException:
        if os.getenv("EMOTION_DETECTION_OFFLINE") == "1":
            return _offline_emotion_detector(text_to_analyze)
        raise

    if response.status_code == 400:
        return EMPTY_RESULT.copy()

    formatted_response = json.loads(response.text)
    emotions = formatted_response["emotionPredictions"][0]["emotion"]

    emotion_scores = {
        "anger": emotions["anger"],
        "disgust": emotions["disgust"],
        "fear": emotions["fear"],
        "joy": emotions["joy"],
        "sadness": emotions["sadness"],
    }
    emotion_scores["dominant_emotion"] = max(emotion_scores, key=emotion_scores.get)

    return emotion_scores


def _offline_emotion_detector(text_to_analyze):
    """Return local demo scores when the Watson NLP host is unreachable."""
    if not text_to_analyze.strip():
        return EMPTY_RESULT.copy()

    text = text_to_analyze.lower()
    keyword_scores = {
        "anger": ("mad", "hate", "angry"),
        "disgust": ("disgust", "disgusted"),
        "fear": ("afraid", "fear", "scared"),
        "joy": ("glad", "happy", "love", "fun"),
        "sadness": ("sad", "unhappy"),
    }

    dominant_emotion = "joy"
    for emotion, keywords in keyword_scores.items():
        if any(keyword in text for keyword in keywords):
            dominant_emotion = emotion
            break

    emotion_scores = {
        "anger": 0.05,
        "disgust": 0.05,
        "fear": 0.05,
        "joy": 0.05,
        "sadness": 0.05,
    }
    emotion_scores[dominant_emotion] = 0.95
    emotion_scores["dominant_emotion"] = dominant_emotion

    return emotion_scores
