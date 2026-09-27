# ============================================================
# SPEECH & EMOTION ANALYSIS
# CNN + NLP EMOTION MODEL TRAINING
# ============================================================

import os
import json
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Input,
    Embedding,
    Conv1D,
    GlobalMaxPooling1D,
    Dense,
    Dropout
)
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


# ============================================================
# SETTINGS
# ============================================================

MAX_WORDS = 5000
MAX_LENGTH = 20
EMOTION_COUNT = 6
EPOCHS = 30

MODEL_FILE = "emotion_cnn_model.keras"
TOKENIZER_FILE = "tokenizer.json"


# ============================================================
# TENSORFLOW VERSION
# ============================================================

print("=" * 55)
print("🧠 SPEECH & EMOTION ANALYSIS")
print("=" * 55)

print("TensorFlow version:", tf.__version__)


# ============================================================
# TRAINING DATA
# ============================================================

texts = [

    # HAPPY
    "I am very happy",
    "I am feeling great",
    "Today is a wonderful day",
    "I am extremely excited",

    # SAD
    "I am very sad",
    "I feel lonely",
    "I am feeling depressed",
    "Today is a terrible day",

    # ANGRY
    "I am very angry",
    "I hate this",
    "I am furious",
    "This makes me angry",

    # FEAR
    "I am scared",
    "I am afraid",
    "I feel nervous",
    "I am worried",

    # SURPRISE
    "Wow this is amazing",
    "I am shocked",
    "I cannot believe this",

    # NEUTRAL
    "I am okay",
    "Everything is normal",
    "I feel fine"
]


# ============================================================
# LABELS
# ============================================================

labels = [

    # HAPPY = 0
    0, 0, 0, 0,

    # SAD = 1
    1, 1, 1, 1,

    # ANGRY = 2
    2, 2, 2, 2,

    # FEAR = 3
    3, 3, 3, 3,

    # SURPRISE = 4
    4, 4, 4,

    # NEUTRAL = 5
    5, 5, 5
]


# ============================================================
# EMOTION NAMES
# ============================================================

emotion_names = [
    "Happy 😊",
    "Sad 😢",
    "Angry 😠",
    "Fear 😨",
    "Surprise 😲",
    "Neutral 😐"
]


# ============================================================
# CHECK DATA
# ============================================================

print("\n📊 Checking training data...")

print("Total texts :", len(texts))
print("Total labels:", len(labels))

if len(texts) != len(labels):
    raise ValueError(
        f"❌ Data mismatch! Texts={len(texts)}, Labels={len(labels)}"
    )

print("✅ Dataset is valid")


# ============================================================
# TOKENIZATION
# ============================================================

print("\n🔤 Preparing NLP Tokenizer...")

tokenizer = Tokenizer(
    num_words=MAX_WORDS,
    oov_token="<OOV>"
)

tokenizer.fit_on_texts(texts)

sequences = tokenizer.texts_to_sequences(texts)

X = pad_sequences(
    sequences,
    maxlen=MAX_LENGTH,
    padding="post",
    truncating="post"
)


# ============================================================
# LABEL ENCODING
# ============================================================

y = tf.keras.utils.to_categorical(
    labels,
    num_classes=EMOTION_COUNT
)


print("Vocabulary size:", len(tokenizer.word_index))
print("Input shape:", X.shape)
print("Output shape:", y.shape)


# ============================================================
# CNN MODEL
# ============================================================

print("\n🏗️ Building CNN model...")


model = Sequential([

    # Explicit Input layer
    Input(shape=(MAX_LENGTH,)),

    # Word Embedding
    Embedding(
        input_dim=MAX_WORDS,
        output_dim=64
    ),

    # CNN feature extraction
    Conv1D(
        filters=128,
        kernel_size=3,
        activation="relu"
    ),

    # Extract strongest feature
    GlobalMaxPooling1D(),

    # Fully connected layer
    Dense(
        64,
        activation="relu"
    ),

    # Prevent overfitting
    Dropout(0.3),

    # 6 emotion classes
    Dense(
        EMOTION_COUNT,
        activation="softmax"
    )
])


# ============================================================
# COMPILE MODEL
# ============================================================

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


# ============================================================
# MODEL SUMMARY
# ============================================================

print("\n📋 CNN MODEL SUMMARY\n")

model.summary()


# ============================================================
# TRAIN MODEL
# ============================================================

print("\n" + "=" * 55)
print("🧠 STARTING CNN EMOTION MODEL TRAINING")
print("=" * 55)

history = model.fit(
    X,
    y,
    epochs=EPOCHS,
    batch_size=4,
    shuffle=True,
    verbose=1
)


# ============================================================
# SAVE MODEL
# ============================================================

print("\n💾 Saving CNN model...")

model.save(MODEL_FILE)

print("✅ Model saved successfully:")
print("   📁", MODEL_FILE)


# ============================================================
# SAVE TOKENIZER
# ============================================================

print("\n💾 Saving NLP tokenizer...")

tokenizer_json = tokenizer.to_json()

with open(
    TOKENIZER_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(tokenizer_json)


print("✅ Tokenizer saved successfully:")
print("   📁", TOKENIZER_FILE)


# ============================================================
# FINAL TRAINING RESULT
# ============================================================

final_accuracy = history.history["accuracy"][-1]
final_loss = history.history["loss"][-1]

print("\n" + "=" * 55)
print("🎉 CNN MODEL TRAINED SUCCESSFULLY!")
print("=" * 55)

print(f"📈 Final Training Accuracy: {final_accuracy:.4f}")
print(f"📉 Final Training Loss    : {final_loss:.4f}")

print("\n😊 Supported Emotions:")

for i, emotion in enumerate(emotion_names):
    print(f"   {i} → {emotion}")

print("\n📁 Generated files:")
print(f"   ✅ {MODEL_FILE}")
print(f"   ✅ {TOKENIZER_FILE}")

print("\n🚀 Training completed!")
print("=" * 55)