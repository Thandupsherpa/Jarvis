import speech_recognition as sr  # type: ignore
import webbrowser
import pyttsx3  # type: ignore
import musicLibrary  # your own music dict file
import os
from dotenv import load_dotenv  # type: ignore
import google.generativeai as genai

# Load environment variables
load_dotenv()
geminiapi = os.getenv("GEMINI_API_KEY")

# Initialize Gemini
genai.configure(api_key=geminiapi)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")



# Initialize speech engine and recognizer
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Use Gemini to interpret commands intelligently
def interpret_command_with_gemini(command):
    prompt = f"""
    You are an assistant. Based on the user's voice command: "{command}", classify the intent as one of:
    - open_youtube
    - open_google
    - open_github
    - open_drive
    - open_chatgpt
    - search_google:<query>
    - play_music:<songname>
    - stop
    - unknown

    Just reply with the intent label only. No explanation. No formatting.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip().lower()
    except Exception as e:
        speak("There was an error understanding your command.")
        print(f"Gemini Error: {e}")
        return "unknown"

if __name__ == "__main__":
    speak("Initializing Jarvis with Gemini AI")
    speak("How may I help you?")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            command = command.lower()

            # Get intent using Gemini
            result = interpret_command_with_gemini(command)

            if result == "stop" or result == "exit":
                speak("Goodbye!")
                break

            elif result == "open_youtube":
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")

            elif result == "open_google":
                speak("Opening Google")
                webbrowser.open("https://www.google.com")

            elif result == "open_github":
                speak("Opening your GitHub profile")
                webbrowser.open("https://github.com/Thandupsherpa")

            elif result == "open_drive":
                speak("Opening Drive")
                webbrowser.open("https://drive.google.com/drive/u/1/home")

            elif result == "open_chatgpt":
                speak("Opening ChatGPT")
                webbrowser.open("https://chatgpt.com/")

            elif result.startswith("search_google:"):
                query = result.split(":", 1)[1].strip()
                speak(f"Searching Google for {query}")
                webbrowser.open(f"https://www.google.com/search?q={query}")

            elif result.startswith("play_music:"):
                song = result.split(":", 1)[1].strip()
                link = musicLibrary.music.get(song)
                if link:
                    speak(f"Playing {song}")
                    webbrowser.open(link)
                else:
                    speak("Sorry, I couldn't find that song.")

            else:
                speak("Sorry, I don't understand that command.")

        except sr.UnknownValueError:
            print("Could not understand audio.")
            speak("Sorry, I didn't catch that.")

        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak("Speech recognition service is down.")

        except KeyboardInterrupt:
            speak("Exiting. Goodbye!")
            break
