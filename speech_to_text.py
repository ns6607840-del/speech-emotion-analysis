import speech_recognition as sr


def speech_to_text():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            print("\nAdjusting microphone...")
            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print("✅ Microphone ready!")
            print("🎤 Speak now...")

            audio = recognizer.listen(
                source,
                timeout=10,
                phrase_time_limit=10
            )

        print("\n🔄 Converting speech to text...")

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("✅ You said:")
        print(text)

        return text

    except sr.WaitTimeoutError:

        print("\n❌ No speech detected.")
        print("Please speak within 10 seconds.")

        return ""

    except sr.UnknownValueError:

        print("\n❌ Voice was detected, but words could not be understood.")
        print("👉 Please speak slowly and clearly.")

        return ""

    except sr.RequestError as e:

        print("\n❌ Google Speech Recognition service error:")
        print(e)

        return ""

    except Exception as e:

        print("\n❌ Microphone/System error:")
        print(e)

        return ""


if __name__ == "__main__":
    speech_to_text()