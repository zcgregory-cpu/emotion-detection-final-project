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
