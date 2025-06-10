import speech_recognition as sr # type: ignore
import webbrowser
import pyttsx3 # type: ignore
import musicLibrary 
import requests
import os
from dotenv import load_dotenv # type: ignore


recognizer = sr.Recognizer()
engine = pyttsx3.init()
load_dotenv()
newsapi = os.getenv("NEWS_API_KEY")
gemimiapi = os.getenv("GEMINI_API_KEY")

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
                
            elif "open drive" in command:
                speak("Opening drive")
                webbrowser.open("https://drive.google.com/drive/u/1/home")
                
            elif "open chatgpt" in command:
                speak("opening chatgpt")
                webbrowser.open("https://chatgpt.com/")
                
            elif "search for" in command:
                search_query = command.replace("search for", "").strip()
                speak(f"Searching Google for {search_query}")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                
            elif command.lower().startswith("play"):
                song = command.lower().split(" ")[1]
                link = musicLibrary.music[song]
                webbrowser.open(link)
                
            
            elif "news" in command.lower():
                 r = requests.get(f"https://newsapi.org/v2/everything?q=tesla&from=2025-05-10&sortBy=publishedAt&apiKey={newsapi}")
   
                 if r.status_code == 200:
                     data = r.json()
                     articles = data.get('articles', [])
                     if not articles:
                         speak("Sorry, I couldn't find any Tesla news right now.")
            
                     else:
                         speak("Here are the latest Tesla news headlines.")
                         for article in articles[:10]:
                             speak(article['title'])# limit to top 5
                 else:
                     
                     speak("Sorry, I wasn't able to fetch the news.")
                     
                          
        
            
           
        
    

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
