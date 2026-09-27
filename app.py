# ============================================================
# EMOTIVOICE AI
# SPEECH & EMOTIONAL ANALYSIS SYSTEM
# CNN + NLP
# ============================================================

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

import numpy as np
import os
import json


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

# Allow frontend (React/HTML/JS) to communicate with Flask
CORS(app)


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# MODEL SETTINGS
# ============================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "emotion_cnn_model.keras"
)

TOKENIZER_PATH = os.path.join(
    BASE_DIR,
    "tokenizer.json"
)


# ============================================================
# DEFAULT MAX LENGTH
# ============================================================

MAX_LENGTH = 20


# ============================================================
# EMOTION LABELS
#
# IMPORTANT:
# These labels MUST be in the same order as training.
# ============================================================

EMOTIONS = [
    "Happy",
    "Sad",
    "Angry",
    "Fear",
    "Surprise",
    "Neutral"
]


# ============================================================
# GLOBAL VARIABLES
# ============================================================

cnn_model = None
tokenizer = None


# ============================================================
# NLP EMOTION DETECTOR
# ============================================================

def detect_emotion(text):

    text = text.lower().strip()

    # -------------------------
    # Happy
    # -------------------------

    happy_words = [
        "happy",
        "joy",
        "good",
        "great",
        "awesome",
        "excellent",
        "love",
        "lovely",
        "wonderful",
        "amazing",
        "excited",
        "fun",
        "glad",
        "smile",
        "smiling",
        "best"
    ]

    # -------------------------
    # Sad
    # -------------------------

    sad_words = [
        "sad",
        "unhappy",
        "cry",
        "crying",
        "depressed",
        "lonely",
        "alone",
        "hurt",
        "pain",
        "bad",
        "upset",
        "sorry",
        "miss",
        "missing",
        "broken"
    ]

    # -------------------------
    # Angry
    # -------------------------

    angry_words = [
        "angry",
        "anger",
        "mad",
        "hate",
        "furious",
        "annoyed",
        "annoying",
        "irritated",
        "rage",
        "fight",
        "stupid",
        "worst"
    ]

    # -------------------------
    # Fear
    # -------------------------

    fear_words = [
        "fear",
        "afraid",
        "scared",
        "scary",
        "terrified",
        "terror",
        "worried",
        "worry",
        "nervous",
        "danger",
        "dangerous",
        "panic"
    ]

    # -------------------------
    # Surprise
    # -------------------------

    surprise_words = [
        "wow",
        "surprise",
        "surprised",
        "shocked",
        "shock",
        "unexpected",
        "unbelievable",
        "suddenly",
        "really"
    ]

    # -------------------------
    # Check emotions
    # -------------------------

    for word in happy_words:
        if word in text:
            return "Happy"

    for word in sad_words:
        if word in text:
            return "Sad"

    for word in angry_words:
        if word in text:
            return "Angry"

    for word in fear_words:
        if word in text:
            return "Fear"

    for word in surprise_words:
        if word in text:
            return "Surprise"

    return "Neutral"


# ============================================================
# LOAD CNN MODEL
# ============================================================

def load_cnn_model():

    global cnn_model

    if not os.path.exists(MODEL_PATH):

        print("⚠️ CNN model not found:")
        print(MODEL_PATH)

        cnn_model = None
        return

    try:

        cnn_model = load_model(
            MODEL_PATH,
            compile=False
        )

        print("✅ CNN model loaded successfully!")

        try:

            print(
                "📐 Model input shape:",
                cnn_model.input_shape
            )

            print(
                "📐 Model output shape:",
                cnn_model.output_shape
            )

        except Exception:
            pass

    except Exception as e:

        cnn_model = None

        print("❌ CNN model loading error:")
        print(str(e))


# ============================================================
# LOAD TOKENIZER
# ============================================================

def load_tokenizer():

    global tokenizer

    if not os.path.exists(TOKENIZER_PATH):

        print("⚠️ tokenizer.json not found:")
        print(TOKENIZER_PATH)

        tokenizer = None
        return

    try:

        with open(
            TOKENIZER_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            tokenizer_json = file.read()

        tokenizer = tokenizer_from_json(
            tokenizer_json
        )

        print("✅ NLP tokenizer loaded successfully!")

    except Exception as e:

        tokenizer = None

        print("❌ Tokenizer loading error:")
        print(str(e))


# ============================================================
# LOAD EVERYTHING
# ============================================================

load_cnn_model()
load_tokenizer()


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/", methods=["GET"])
def home():

    try:

        return render_template(
            "index.html"
        )

    except Exception:

        return jsonify({

            "success": True,

            "message":
            "EMOTIVOICE AI Backend is running!",

            "api":
            "/analyze",

            "model":
            "CNN + NLP"

        })


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({

        "success": True,

        "message":
        "Backend is running",

        "cnn_model":
        cnn_model is not None,

        "tokenizer":
        tokenizer is not None

    })


# ============================================================
# ANALYZE EMOTION
# ============================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    try:

        # ----------------------------------------------------
        # GET JSON
        # ----------------------------------------------------

        data = request.get_json(
            silent=True
        )

        if not data:

            return jsonify({

                "success": False,

                "message":
                "No JSON data received."

            }), 400


        # ----------------------------------------------------
        # GET TEXT
        # ----------------------------------------------------

        text = data.get(
            "text",
            ""
        )

        if not isinstance(text, str):

            return jsonify({

                "success": False,

                "message":
                "Text must be a string."

            }), 400


        text = text.strip()


        # ----------------------------------------------------
        # EMPTY TEXT
        # ----------------------------------------------------

        if not text:

            return jsonify({

                "success": False,

                "message":
                "Please enter or speak a sentence."

            }), 400


        # ----------------------------------------------------
        # NLP PREDICTION
        # ----------------------------------------------------

        nlp_emotion = detect_emotion(
            text
        )


        # ----------------------------------------------------
        # DEFAULT RESULT
        # ----------------------------------------------------

        final_emotion = nlp_emotion

        cnn_emotion = "Not Available"

        confidence = 0.0


        # ----------------------------------------------------
        # CNN PREDICTION
        # ----------------------------------------------------

        if (
            cnn_model is not None
            and tokenizer is not None
        ):

            try:

                # Convert text to sequence
                sequence = tokenizer.texts_to_sequences(
                    [text]
                )


                # --------------------------------------------
                # Determine max length
                # --------------------------------------------

                model_max_length = MAX_LENGTH

                try:

                    input_shape = cnn_model.input_shape

                    if (
                        isinstance(input_shape, tuple)
                        and len(input_shape) >= 2
                        and isinstance(input_shape[1], int)
                    ):

                        model_max_length = input_shape[1]

                except Exception:

                    model_max_length = MAX_LENGTH


                # --------------------------------------------
                # Pad sequence
                # --------------------------------------------

                padded_text = pad_sequences(

                    sequence,

                    maxlen=model_max_length,

                    padding="post",

                    truncating="post"

                )


                # --------------------------------------------
                # CNN prediction
                # --------------------------------------------

                prediction = cnn_model.predict(

                    padded_text,

                    verbose=0

                )


                # --------------------------------------------
                # Convert prediction to numpy array
                # --------------------------------------------

                prediction = np.asarray(
                    prediction
                )


                # --------------------------------------------
                # Flatten output
                # --------------------------------------------

                if prediction.ndim > 1:

                    probabilities = prediction[0]

                else:

                    probabilities = prediction


                probabilities = np.asarray(
                    probabilities,
                    dtype=float
                ).flatten()


                # --------------------------------------------
                # Validate prediction
                # --------------------------------------------

                if len(probabilities) == 0:

                    raise ValueError(
                        "CNN returned an empty prediction."
                    )


                # --------------------------------------------
                # Get highest probability
                # --------------------------------------------

                emotion_index = int(
                    np.argmax(
                        probabilities
                    )
                )


                # --------------------------------------------
                # Check emotion index
                # --------------------------------------------

                if (
                    emotion_index >= 0
                    and
                    emotion_index < len(EMOTIONS)
                ):

                    cnn_emotion = EMOTIONS[
                        emotion_index
                    ]

                else:

                    cnn_emotion = "Unknown"


                # --------------------------------------------
                # Confidence
                # --------------------------------------------

                confidence = float(
                    np.max(
                        probabilities
                    ) * 100
                )


                # --------------------------------------------
                # Final emotion
                # --------------------------------------------

                final_emotion = cnn_emotion


            except Exception as cnn_error:

                print(
                    "⚠️ CNN prediction error:",
                    str(cnn_error)
                )

                # If CNN fails, use NLP result
                final_emotion = nlp_emotion

                cnn_emotion = "Prediction Error"

                confidence = 0.0


        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "text": text,

            "emotion": final_emotion,

            "confidence":
            round(
                confidence,
                2
            ),

            "nlp_emotion":
            nlp_emotion,

            "cnn_emotion":
            cnn_emotion

        })


    except Exception as e:

        print(
            "❌ Analyze error:",
            str(e)
        )

        return jsonify({

            "success": False,

            "message":
            "Something went wrong while analyzing emotion.",

            "error":
            str(e)

        }), 500


# ============================================================
# SPEECH ROUTE
# ============================================================

@app.route(
    "/listen",
    methods=["GET"]
)
def listen():

    return jsonify({

        "success": True,

        "message":
        "Browser speech recognition is handled by the frontend."

    })


# ============================================================
# MODEL STATUS
# ============================================================

@app.route(
    "/model-status",
    methods=["GET"]
)
def model_status():

    return jsonify({

        "success": True,

        "model":
        "CNN + NLP",

        "status":
        "Loaded"
        if cnn_model is not None
        else "Not Loaded",

        "model_file":
        MODEL_PATH,

        "model_exists":
        os.path.exists(
            MODEL_PATH
        ),

        "tokenizer":
        "Loaded"
        if tokenizer is not None
        else "Not Loaded",

        "tokenizer_exists":
        os.path.exists(
            TOKENIZER_PATH
        )

    })


# ============================================================
# CNN TEST
# ============================================================

@app.route(
    "/cnn-test",
    methods=["GET"]
)
def cnn_test():

    if cnn_model is None:

        return jsonify({

            "success": False,

            "message":
            "CNN model is not loaded."

        }), 500


    if tokenizer is None:

        return jsonify({

            "success": False,

            "message":
            "Tokenizer is not loaded."

        }), 500


    try:

        # ----------------------------------------------------
        # Test sentence
        # ----------------------------------------------------

        test_text = (
            "I am very happy today"
        )


        # ----------------------------------------------------
        # Convert text
        # ----------------------------------------------------

        sequence = tokenizer.texts_to_sequences(
            [test_text]
        )


        # ----------------------------------------------------
        # Get model input length
        # ----------------------------------------------------

        model_max_length = MAX_LENGTH

        try:

            input_shape = cnn_model.input_shape

            if (
                isinstance(input_shape, tuple)
                and len(input_shape) >= 2
                and isinstance(input_shape[1], int)
            ):

                model_max_length = input_shape[1]

        except Exception:

            pass


        # ----------------------------------------------------
        # Padding
        # ----------------------------------------------------

        padded_text = pad_sequences(

            sequence,

            maxlen=model_max_length,

            padding="post",

            truncating="post"

        )


        # ----------------------------------------------------
        # Prediction
        # ----------------------------------------------------

        prediction = cnn_model.predict(

            padded_text,

            verbose=0

        )


        prediction = np.asarray(
            prediction
        )


        if prediction.ndim > 1:

            probabilities = prediction[0]

        else:

            probabilities = prediction


        probabilities = np.asarray(
            probabilities,
            dtype=float
        ).flatten()


        # ----------------------------------------------------
        # Emotion
        # ----------------------------------------------------

        emotion_index = int(
            np.argmax(
                probabilities
            )
        )


        if (
            emotion_index >= 0
            and
            emotion_index < len(EMOTIONS)
        ):

            emotion = EMOTIONS[
                emotion_index
            ]

        else:

            emotion = "Unknown"


        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        confidence = float(

            np.max(
                probabilities
            ) * 100

        )


        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "test_text":
            test_text,

            "emotion":
            emotion,

            "confidence":
            round(
                confidence,
                2
            ),

            "model_output":
            probabilities.tolist()

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "message":
            "CNN test failed.",

            "error":
            str(e)

        }), 500


# ============================================================
# SERVER
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)

    print(
        "🎤 EMOTIVOICE AI"
    )

    print(
        "Speech & Emotional Analysis System"
    )

    print("=" * 60)


    # --------------------------------------------------------
    # CNN STATUS
    # --------------------------------------------------------

    if cnn_model is not None:

        print(
            "🤖 CNN Emotion Model: READY"
        )

    else:

        print(
            "⚠️ CNN Emotion Model: NOT READY"
        )


    # --------------------------------------------------------
    # TOKENIZER STATUS
    # --------------------------------------------------------

    if tokenizer is not None:

        print(
            "🔤 NLP Tokenizer: READY"
        )

    else:

        print(
            "⚠️ NLP Tokenizer: NOT READY"
        )


    # --------------------------------------------------------
    # NLP STATUS
    # --------------------------------------------------------

    print(
        "🧠 NLP Emotion Detector: READY"
    )


    # --------------------------------------------------------
    # SERVER
    # --------------------------------------------------------

    print(
        "🌐 Server:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print("=" * 60)


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )