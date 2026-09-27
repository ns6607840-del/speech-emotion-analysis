# ============================================================
# EMOTIVOICE AI
# NLP EMOTION DETECTOR
# ============================================================

import re


EMOTIONS = {
    "Happy": [
        "happy",
        "joy",
        "great",
        "good",
        "awesome",
        "excellent",
        "excited",
        "love",
        "wonderful",
        "amazing",
        "glad",
        "fantastic",
        "pleased"
    ],

    "Sad": [
        "sad",
        "unhappy",
        "depressed",
        "cry",
        "crying",
        "lonely",
        "upset",
        "hurt",
        "bad",
        "miss",
        "missed",
        "unfortunate"
    ],

    "Angry": [
        "angry",
        "mad",
        "furious",
        "hate",
        "annoyed",
        "irritated",
        "rage",
        "stupid",
        "frustrated",
        "frustrating"
    ],

    "Fear": [
        "afraid",
        "fear",
        "scared",
        "frightened",
        "worried",
        "nervous",
        "danger",
        "terrified",
        "panic",
        "anxious"
    ],

    "Surprise": [
        "surprised",
        "surprise",
        "shocked",
        "wow",
        "unexpected",
        "amazing",
        "unbelievable",
        "really"
    ],

    "Neutral": [
        "okay",
        "fine",
        "normal",
        "nothing",
        "alright",
        "maybe",
        "yes",
        "no",
        "sure"
    ]
}


def detect_emotion(text):

    text = text.lower().strip()

    scores = {}

    for emotion, words in EMOTIONS.items():

        score = 0

        for word in words:

            # Whole-word matching
            if re.search(r"\b" + re.escape(word) + r"\b", text):
                score += 1

        scores[emotion] = score

    detected_emotion = max(
        scores,
        key=scores.get
    )

    # If no emotion word is detected
    if scores[detected_emotion] == 0:
        detected_emotion = "Neutral"

    return detected_emotion


if __name__ == "__main__":

    print("=" * 50)
    print("        EMOTIVOICE AI")
    print("        TEXT EMOTION DETECTOR")
    print("=" * 50)

    text = input("\nEnter a sentence: ")

    emotion = detect_emotion(text)

    print("\nText:", text)
    print("Detected Emotion:", emotion)