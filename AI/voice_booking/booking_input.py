import speech_recognition as sr


def speech_to_text(language="en-IN"):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n🎤 Speak your booking request...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
        return text

    except sr.UnknownValueError:
        print("❌ Could not understand your speech.")
        return None

    except sr.RequestError as e:
        print("❌ Speech recognition error:", e)
        return None


def get_booking_input():
    print("\nChoose how you want to book:")
    print("1. Type")
    print("2. Speak")

    choice = input("Enter 1 or 2: ")

    if choice == "1":
        # Text input
        text = input("\n⌨️ Enter your booking request: ")
        return text

    elif choice == "2":
        # Voice input
        language = input(
            "\nLanguage (en-IN / hi-IN): "
        ).strip()

        if not language:
            language = "en-IN"

        return speech_to_text(language)

    else:
        print("❌ Invalid choice.")
        return None


if __name__ == "__main__":

    user_text = get_booking_input()

    if user_text:
        print("\n✅ Booking Request:")
        print(user_text)