import speech_recognition as sr
import webbrowser
import pyttsx3


recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()
    

    


if __name__ == "__main__":
    speak("Initializing Jarvis")
    speak("How may i help you")
    
        
    

    while True:
        try:
            
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            command = command.lower()

            
            if "stop" in command or "exit" in command:
                speak("Goodbye!")
                break

            elif "open youtube" in command:
                speak("Opening YouTube")
                webbrowser.open("https://www.youtube.com")

            elif "open google" in command:
                speak("Opening Google")
                webbrowser.open("https://www.google.com")
                
            elif "open github" in command:
                speak("Opening your github profile")
                webbrowser.open("https://github.com/Thandupsherpa")

            elif "search for" in command:
                search_query = command.replace("search for", "").strip()
                speak(f"Searching Google for {search_query}")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")

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
