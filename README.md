# 🎤 Speech & Emotion Analysis Using CNN and NLP

## 📌 Project Overview

Speech & Emotion Analysis is an Artificial Intelligence and Machine
Learning based web application that analyzes a user's speech or text
and identifies the emotion expressed in the input.

The system combines **Speech-to-Text**, **Natural Language Processing
(NLP)** and a **Convolutional Neural Network (CNN)** based emotion
classification model.

The application provides a simple and interactive web interface where
users can either enter a sentence manually or speak through a
microphone.

---

## 🎯 Objectives

The main objectives of this project are:

- To analyze human speech and text.
- To convert speech into text using Speech Recognition.
- To identify emotions from textual input using NLP.
- To use a CNN-based Machine Learning model for emotion classification.
- To integrate AI/ML models with a web application.
- To provide an easy-to-use emotion analysis interface.
- To demonstrate the practical application of AI and NLP.

---

## 🚀 Features

### 🎤 Speech Input

Users can click the **Start Speaking** button and provide voice input
through their microphone.

### 📝 Text Input

Users can directly type a sentence into the text box for emotion
analysis.

### 🔊 Speech-to-Text

The speech input is converted into text before further processing.

### 🧠 NLP Emotion Detection

Natural Language Processing techniques are used to analyze the
emotional meaning of the entered text.

### 🤖 CNN Emotion Model

A Convolutional Neural Network model is included for emotion
classification.

### 🌐 Web Application

The complete application is connected through a Flask backend and
provides an interactive browser-based interface.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application backend |
| TensorFlow | Machine Learning framework |
| Keras | CNN model development |
| CNN | Emotion classification |
| NLP | Text emotion analysis |
| Speech Recognition | Speech-to-text conversion |
| HTML | Web page structure |
| CSS | User interface styling |
| JavaScript | Frontend interaction |

---

## 🏗️ Project Architecture

```text
                ┌──────────────────────┐
                │       User           │
                └──────────┬───────────┘
                           │
                    Text / Speech
                           │
                           ▼
                ┌──────────────────────┐
                │    Web Interface     │
                │   HTML/CSS/JS        │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Flask Backend     │
                │       app.py         │
                └──────────┬───────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      ┌─────────────────┐      ┌─────────────────┐
      │ Speech-to-Text  │      │   NLP Emotion   │
      │                 │      │    Detector     │
      └────────┬────────┘      └────────┬────────┘
               │                        │
               └────────────┬───────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │   CNN Emotion    │
                  │      Model       │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Emotion Result   │
                  └──────────────────┘