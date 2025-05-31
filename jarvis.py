import re
import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import requests
from bs4 import BeautifulSoup 
import time
import pyautogui
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def greet():
    hour = int(datetime.datetime.now().hour)
    if 0 < hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 17:
        speak("Good Afternoon")
    elif 17 <= hour < 21:
        speak("Good Evening")
    else:
        speak("Good Night")
    speak("How can I help you?")
def commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300  
        audio = r.listen(source,timeout=5, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print("User said:", query)
        return query
    except Exception as e:
        print("Error:", e)
        speak("Say that again please")
        return None
def extract_city(query):
    # Try to extract city name using common patterns
    match = re.search(r"(?:temperature|weather) in ([a-zA-Z\s]+)", query)
    if match:
        return match.group(1).strip()
    else:
        return None
def setAlarm(Query):
    timehere=open("time.txt","a")
    timehere.write(Query)
    timehere.close()
    os.startfile("alarm.py")

greet()
while True:
    query = commands()
    if query is None:
        continue
    query = query.lower()
    if "wikipedia" in query:
        speak("Searching in Wikipedia...")
        query = query.replace("wikipedia", " ")
        try:
            results = wikipedia.summary(query, sentences=1)
            speak("According to Wikipedia")
            speak(results)
        except Exception as e:
            print("Wikipedia error:", e)
            speak("Sorry, I couldn't find anything.")
    elif "youtube" in query:
        webbrowser.open("youtube.com")
        time.sleep(3)
    elif "google" in query:
        webbrowser.open("google.com")
        time.sleep(3)
    elif "play music" in query:
        musicdir="d:\\Music"
        songs=os.listdir(musicdir)
        print(songs)
        os.startfile(os.path.join(musicdir,songs[3]))
        time.sleep(3)
    elif "code" in query:
        codepath="C:\\Users\\tharu\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codepath)
        time.sleep(3)
    elif "chrome" in query:
        codepath1="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(codepath1)
        time.sleep(3)
    elif "time" in query:
        time=datetime.datetime.now().strftime("%H:%M")
        speak(time)
    elif "set an alarm" in query:
        speak("set the time")
        a=input("Please tell the time:")
        setAlarm(a)
        speak("done sir")
    elif "pause" in query:
        pyautogui.press("k")
        speak("video paused")
    elif "play" in query:
        pyautogui.press("k")
        speak("video played")
    elif "mute" in query:
        pyautogui.press("m")
        speak("video muted")
    elif "volume up" in query:
        from keyboard import volumeUp
        speak("Turning volume up")
        volumeUp()
    elif "volume down" in query:
        from keyboard import volumeDown
        speak("Turning volume down")
        volumeDown()
    elif "shutdown system" in query:
        speak("Do you really want to shut down the system?")
        s = input("Type 'yes' to confirm shutdown: ").lower()
        if s == "yes":
            speak("Shutting down the system now.")
            os.system("shutdown /s /t 1")  # ✅ Corrected command
        else:
            speak("Shutdown cancelled.")
    elif "screenshot" in query:
        im=pyautogui.screenshot()
        im.save("ss.jpg")
    elif "click photo" in query:
        pyautogui.press("super")
        pyautogui.typewrite("camera")
        pyautogui.press("enter")
        pyautogui.sleep(2)
        speak("smile")
        pyautogui.press("enter")
    elif "temperature" in query:
        #city="chennai"
        city = extract_city(query)
        if not city:
            speak("Please specify a city name.")
        url=f"https://api.openweathermap.org/data/2.5/weather?&units=metric&appid=9b345ac3061cc8c45a7a08562baccb1b&q={city}"
        r=requests.get(url)
        d=r.json()
        temp=d["main"]["temp"]
        if temp:
            speak(f"current temperature in {city} is {temp}")
        else:
            speak("I could not find")
    elif "weather" in query:
        # city="chennai"
        url=f"https://api.openweathermap.org/data/2.5/weather?&units=metric&appid=9b345ac3061cc8c45a7a08562baccb1b&q={city}"
        r=requests.get(url)
        d=r.json()
        temp=d["main"]["temp"]
        if temp:
            speak(f"current temperature in {city} is {temp} in degree celsius")
        else:
            speak("I could not find")
    if "exit" in query or "quit" in query:
        speak("Goodbye!")
        break