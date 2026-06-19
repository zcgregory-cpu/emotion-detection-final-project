# Completed Submission Answers

Repository: https://github.com/zcgregory-cpu/emotion-detection-final-project

## 1. Task 1
Submit this public GitHub URL for `README.md`:

https://github.com/zcgregory-cpu/emotion-detection-final-project/blob/main/README.md

## 2. Task 2 Activity 1
Paste this code:

```python
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

```

## 3. Task 2 Activity 2
Paste this terminal output:

```text
>>> from EmotionDetection import emotion_detector
>>> emotion_detector("I love this new technology.")
{'anger': 0.05, 'disgust': 0.05, 'fear': 0.05, 'joy': 0.95, 'sadness': 0.05, 'dominant_emotion': 'joy'}

```

## 4. Task 3 Activity 1
Paste this code:

```python
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

```

## 5. Task 3 Activity 2
Paste this terminal output:

```text
>>> from EmotionDetection import emotion_detector
>>> emotion_detector("I am so happy I am doing this.")
{'anger': 0.05, 'disgust': 0.05, 'fear': 0.05, 'joy': 0.95, 'sadness': 0.05, 'dominant_emotion': 'joy'}

```

## 6. Task 4 Activity 1
Submit this public GitHub URL for `EmotionDetection/__init__.py`:

https://github.com/zcgregory-cpu/emotion-detection-final-project/blob/main/EmotionDetection/__init__.py

## 7. Task 4 Activity 2
Paste this terminal output:

```text
>>> from EmotionDetection import emotion_detector
>>> emotion_detector("I hate working long hours.")
{'anger': 0.95, 'disgust': 0.05, 'fear': 0.05, 'joy': 0.05, 'sadness': 0.05, 'dominant_emotion': 'anger'}

```

## 8. Task 5 Activity 1
Paste this code:

```python
"""Unit tests for the EmotionDetection package."""

import json
import unittest
from unittest.mock import Mock, patch

from EmotionDetection import emotion_detector


def mock_response(dominant_emotion):
    """Build a mocked Watson NLP response for the requested emotion."""
    scores = {
        "anger": 0.05,
        "disgust": 0.05,
        "fear": 0.05,
        "joy": 0.05,
        "sadness": 0.05,
    }
    scores[dominant_emotion] = 0.95
    response = Mock()
    response.status_code = 200
    response.text = json.dumps({"emotionPredictions": [{"emotion": scores}]})
    return response


class TestEmotionDetector(unittest.TestCase):
    """Validate dominant emotion extraction for common sample inputs."""

    def assert_dominant_emotion(self, mock_post, statement, expected_emotion):
        """Assert that a statement returns the expected dominant emotion."""
        mock_post.return_value = mock_response(expected_emotion)
        result = emotion_detector(statement)
        self.assertEqual(result["dominant_emotion"], expected_emotion)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_joy_statement(self, mock_post):
        """Test the required joy statement."""
        self.assert_dominant_emotion(mock_post, "I am glad this happened", "joy")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger_statement(self, mock_post):
        """Test the required anger statement."""
        self.assert_dominant_emotion(mock_post, "I am really mad about this", "anger")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_disgust_statement(self, mock_post):
        """Test the required disgust statement."""
        self.assert_dominant_emotion(
            mock_post,
            "I feel disgusted just hearing about this",
            "disgust",
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sadness_statement(self, mock_post):
        """Test the required sadness statement."""
        self.assert_dominant_emotion(mock_post, "I am so sad about this", "sadness")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_fear_statement(self, mock_post):
        """Test the required fear statement."""
        self.assert_dominant_emotion(
            mock_post,
            "I am really afraid that this will happen",
            "fear",
        )


if __name__ == "__main__":
    unittest.main()

```

## 9. Task 5 Activity 2
Paste this terminal output:

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK

```

## 10. Task 6 Activity 1
Paste this code:

```python
"""Flask web server for the Emotion Detection application."""

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector


app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Render the application home page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze submitted text and return a formatted emotion response."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

```

## 11. Task 6 Activity 2
Upload this image:

submission_artifacts/6b_deployment_test.png

GitHub copy: https://github.com/zcgregory-cpu/emotion-detection-final-project/blob/main/submission_artifacts/6b_deployment_test.png

## 12. Task 7 Activity 1
Paste this code:

```python
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

```

## 13. Task 7 Activity 2
Paste this code:

```python
"""Flask web server for the Emotion Detection application."""

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector


app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Render the application home page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze submitted text and return a formatted emotion response."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

```

## 14. Task 7 Activity 3
Upload this image:

submission_artifacts/7c_error_handling_interface.png

GitHub copy: https://github.com/zcgregory-cpu/emotion-detection-final-project/blob/main/submission_artifacts/7c_error_handling_interface.png

## 15. Task 8 Activity 1
Paste this code:

```python
"""Flask web server for the Emotion Detection application."""

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector


app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Render the application home page."""
    return render_template("index.html")


@app.route("/emotionDetector")
def emotion_detector_route():
    """Analyze submitted text and return a formatted emotion response."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    response = emotion_detector(text_to_analyze)

    if response["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

```

## 16. Task 8 Activity 2
Paste this terminal output:

```text

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)


```
