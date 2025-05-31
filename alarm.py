import pyttsx3
import datetime
import os
import time as t 

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

with open("time.txt", "rt") as extracttime:
    time_set = extracttime.read().strip()

# Clear file after reading
with open("time.txt", "w") as clearfile:
    clearfile.truncate(0)

def ring(time_string):
    time_cleaned = (
        time_string.replace("jarvis", "")
        .replace("set an alarm", "")
        .replace(" and ", ":")
        .strip()
    )

    Alarmtime = time_cleaned
    print(f"Alarm is set for: {Alarmtime}")

    while True:
        currentTime = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Current time: {currentTime}") 

        if currentTime == Alarmtime:
            speak("Alarm ringing sir")
            
            music_path = "Champagini(KoshalWorld.Com).mp3"
            if os.path.exists(music_path):
                os.startfile(music_path)
            else:
                speak("Alarm file not found.")
            break  # Stop loop after playing
        t.sleep(1)  # Prevent CPU overuse

ring(time_set)
