// ============================================================
// EmotiVoice AI - Frontend JavaScript
// Speech + NLP Emotion Analysis
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    const textInput = document.getElementById("textInput");
    const startSpeakingBtn = document.getElementById("startSpeaking");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const clearBtn = document.getElementById("clearBtn");

    const statusMessage = document.getElementById("statusMessage");
    const resultBox = document.getElementById("resultBox");
    const emotionText = document.getElementById("emotionText");
    const confidenceText = document.getElementById("confidenceText");

    // ------------------------------------------------------------
    // Check browser speech recognition support
    // ------------------------------------------------------------

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    let recognition = null;
    let isListening = false;

    if (SpeechRecognition) {

        recognition = new SpeechRecognition();

        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onstart = () => {

            isListening = true;

            if (startSpeakingBtn) {
                startSpeakingBtn.innerHTML = "🎙️ Listening...";
                startSpeakingBtn.classList.add("listening");
            }

            showStatus(
                "🎙️ Listening... Please speak clearly.",
                "info"
            );
        };

        recognition.onresult = (event) => {

            const transcript =
                event.results[0][0].transcript;

            if (textInput) {
                textInput.value = transcript;
            }

            showStatus(
                "✅ Speech converted to text successfully.",
                "success"
            );

            // Automatically analyze speech
            analyzeEmotion();
        };

        recognition.onerror = (event) => {

            console.error(
                "Speech recognition error:",
                event.error
            );

            let message =
                "❌ Speech recognition failed.";

            if (event.error === "not-allowed") {
                message =
                    "❌ Microphone permission denied.";
            }

            if (event.error === "no-speech") {
                message =
                    "⚠️ No speech detected. Please try again.";
            }

            showStatus(message, "error");
        };

        recognition.onend = () => {

            isListening = false;

            if (startSpeakingBtn) {
                startSpeakingBtn.innerHTML =
                    "🎤 Start Speaking";

                startSpeakingBtn.classList.remove(
                    "listening"
                );
            }
        };

    } else {

        console.warn(
            "Speech Recognition is not supported."
        );

        if (startSpeakingBtn) {
            startSpeakingBtn.disabled = true;
            startSpeakingBtn.innerHTML =
                "🎤 Speech Not Supported";
        }
    }


    // ------------------------------------------------------------
    // Start Speaking
    // ------------------------------------------------------------

    if (startSpeakingBtn) {

        startSpeakingBtn.addEventListener(
            "click",
            () => {

                if (!recognition) {

                    showStatus(
                        "❌ Your browser does not support speech recognition.",
                        "error"
                    );

                    return;
                }

                if (isListening) {

                    recognition.stop();

                    return;
                }

                try {

                    recognition.start();

                } catch (error) {

                    console.error(error);

                    showStatus(
                        "⚠️ Speech recognition could not start.",
                        "error"
                    );
                }
            }
        );
    }


    // ------------------------------------------------------------
    // Analyze Emotion Button
    // ------------------------------------------------------------

    if (analyzeBtn) {

        analyzeBtn.addEventListener(
            "click",
            analyzeEmotion
        );
    }


    // ------------------------------------------------------------
    // Clear Button
    // ------------------------------------------------------------

    if (clearBtn) {

        clearBtn.addEventListener(
            "click",
            clearAll
        );
    }


    // ============================================================
    // ANALYZE EMOTION
    // ============================================================

    async function analyzeEmotion() {

        if (!textInput) {
            return;
        }

        const text =
            textInput.value.trim();

        if (!text) {

            showStatus(
                "⚠️ Please enter or speak a sentence first.",
                "error"
            );

            return;
        }


        // Disable button while processing

        if (analyzeBtn) {

            analyzeBtn.disabled = true;

            analyzeBtn.innerHTML =
                "⏳ Analyzing...";
        }


        showStatus(
            "🧠 AI is analyzing your emotion...",
            "info"
        );


        try {

            // ----------------------------------------------------
            // Send text to Flask backend
            // ----------------------------------------------------

            const response = await fetch(
                "/analyze",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })
                }
            );


            const data =
                await response.json();


            // ----------------------------------------------------
            // Backend response
            // ----------------------------------------------------

            if (!response.ok ||
                !data.success) {

                throw new Error(
                    data.message ||
                    "Emotion analysis failed."
                );
            }


            console.log(
                "Backend Response:",
                data
            );


            // ----------------------------------------------------
            // Display result
            // ----------------------------------------------------

            displayResult(
                data.emotion,
                data.confidence
            );


            showStatus(
                "✅ Emotion analysis completed.",
                "success"
            );


        } catch (error) {

            console.error(
                "Analysis Error:",
                error
            );

            showStatus(
                "❌ Could not connect to the backend. Make sure Flask is running.",
                "error"
            );

        } finally {

            if (analyzeBtn) {

                analyzeBtn.disabled = false;

                analyzeBtn.innerHTML =
                    "🔍 Analyze Emotion";
            }
        }
    }


    // ============================================================
    // DISPLAY RESULT
    // ============================================================

    function displayResult(
        emotion,
        confidence
    ) {

        if (resultBox) {

            resultBox.style.display =
                "block";
        }


        if (emotionText) {

            emotionText.textContent =
                emotion || "Neutral";

            // Remove previous classes

            emotionText.classList.remove(
                "happy",
                "sad",
                "angry",
                "fear",
                "surprise",
                "disgust",
                "neutral"
            );


            // Add emotion class

            const emotionClass =
                String(
                    emotion || "neutral"
                )
                    .toLowerCase()
                    .trim();

            emotionText.classList.add(
                emotionClass
            );
        }


        if (confidenceText) {

            if (
                confidence !== undefined &&
                confidence !== null
            ) {

                confidenceText.textContent =
                    `Confidence: ${confidence}%`;

            } else {

                confidenceText.textContent =
                    "AI Emotion Analysis Result";
            }
        }
    }


    // ============================================================
    // STATUS MESSAGE
    // ============================================================

    function showStatus(
        message,
        type
    ) {

        if (!statusMessage) {
            return;
        }

        statusMessage.textContent =
            message;

        statusMessage.className =
            "status-message";

        if (type) {

            statusMessage.classList.add(
                type
            );
        }
    }


    // ============================================================
    // CLEAR EVERYTHING
    // ============================================================

    function clearAll() {

        if (isListening &&
            recognition) {

            recognition.stop();
        }


        if (textInput) {

            textInput.value = "";
        }


        if (resultBox) {

            resultBox.style.display =
                "none";
        }


        if (emotionText) {

            emotionText.textContent = "";
        }


        if (confidenceText) {

            confidenceText.textContent = "";
        }


        showStatus(
            "Ready for a new analysis.",
            "info"
        );
    }

});