import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import os
from dotenv import load_dotenv
import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread


load_dotenv()
geminiapi = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=geminiapi)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")


recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    log(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

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
        log(f"Gemini Error: {e}")
        return "unknown"

def log(message):
    log_box.insert(tk.END, f"{message}\n")
    log_box.see(tk.END)

def process_voice():
    status_label.config(text="Listening...")
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        command = recognizer.recognize_google(audio)
        log(f"You said: {command}")
        command = command.lower()

        result = interpret_command_with_gemini(command)

        if result == "stop" or result == "exit":
            speak("Goodbye!")
            root.quit()

        elif result == "open_youtube":
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif result == "open_google":
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif result == "open_github":
            speak("Opening GitHub")
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
        speak("Sorry, I didn't catch that.")
    except sr.RequestError as e:
        speak("Speech recognition service is down.")
        log(f"Speech Error: {e}")
    finally:
        status_label.config(text="Ready")


def start_listening():
    Thread(target=process_voice).start()


root = tk.Tk()
root.title("Jarvis Assistant")
root.geometry("1000x800")

status_label = tk.Label(root, text="", font=("Helvetica", 14))
status_label.pack(pady=10)

listen_button = tk.Button(root, text="Start Listening", command=start_listening, font=("Helvetica", 12), bg="#4CAF50", fg="white")
listen_button.pack(pady=10)

log_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=60, font=("Courier", 10))
log_box.pack(pady=10)


speak("What can i do for you today?")
root.mainloop()
