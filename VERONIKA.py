import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import requests
import os
import webbrowser
import psutil
import pyautogui
import subprocess

def speak(text):
    print(f"VERONIKA: {text}")
    engine.say(text)
    engine.runAndWait()

# Initialize speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"User: {command}")
            return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
    except sr.RequestError:
        speak("I'm having trouble connecting. Please check your internet.")
    return None

def get_weather(city):
    try:
        api_key = "YOUR_API_KEY"  # Replace with OpenWeatherMap API key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            description = data["weather"][0]["description"]
            return f"Temperature: {temp}°C, Humidity: {humidity}%, Wind Speed: {wind_speed}m/s, Condition: {description}"
        else:
            return "City not found."
    except Exception as e:
        return "Unable to retrieve weather information."

def get_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def open_application(app_name):
    app_paths = {
        "chrome": r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "edge": r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Edge.lnk",
        "notepad": r"C:\\Program Files (x86)\\Notepad++\\notepad++.exe",
        "calculator":r"C:\\Users\\prath\\OneDrive\\Documents\\NetBeansProjects\\calculator.java\\build\\classes\\calculator",
        "camera": r"start microsoft.windows.camera:",
        "whatsapp": r"C:\\Users\\YourUsername\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
        "vscode": r"C:\Users\prath\Downloads\VSCodeUserSetup-x64-1.95.3.exe"
    }

    app_name = app_name.lower()
    
    if app_name in app_paths:
        try:
            if app_name == "camera":
                os.system(app_paths[app_name])
            else:
                subprocess.Popen(app_paths[app_name])
            speak(f"Opening {app_name}")
        except Exception as e:
            speak("Sorry, I couldn't open the application.")
    else:
        speak("Application not found in my database. Please check the name or update my database.")

def close_application(app_name):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if app_name.lower() in process.info['name'].lower():
            psutil.Process(process.info['pid']).terminate()
            speak(f"Closed {app_name}")
            return
    speak("Application not found.")

def adjust_volume(action):
    actions = {
        "increase": "volumeup",
        "decrease": "volumedown",
        "mute": "volumemute"
    }
    if action in actions:
        pyautogui.press(actions[action], presses=5)
        speak(f"Volume {action}d")

def adjust_brightness(level):
    actions = {"increase": "brightnessup", "decrease": "brightnessdown"}
    if level in actions:
        pyautogui.press(actions[level], presses=5)
        speak(f"Brightness {level}d")

def run_veronika():
    speak(get_greeting() + " I am VERONIKA. How can I assist you today?")
    while True:
        command = take_command()
        if command:
            if "time" in command:
                speak(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
            elif "who is" in command or "what is" in command:
                person = command.replace("who is", "").replace("what is", "").strip()
                try:
                    info = wikipedia.summary(person, sentences=2)
                    speak(info)
                except wikipedia.exceptions.DisambiguationError:
                    speak("There are multiple results. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("I couldn't find any information on that topic.")
            elif "play" in command:
                song = command.replace("play", "").strip()
                speak(f"Playing {song}")
                pywhatkit.playonyt(song)
            elif "weather in" in command:
                city = command.replace("weather in", "").strip()
                speak(get_weather(city))
            elif "search" in command:
                query = command.replace("search", "").strip()
                webbrowser.open(f"https://www.google.com/search?q={query}")
                speak("Here are the search results from Google.")
            elif "good morning" in command or "good afternoon" in command or "good evening" in command:
                speak(get_greeting() + " How can I assist you?")
            elif "open" in command:
                open_application(command.replace("open", "").strip())
            elif "close" in command:
                close_application(command.replace("close", "").strip())
            elif "increase volume" in command:
                adjust_volume("increase")
            elif "decrease volume" in command:
                adjust_volume("decrease")
            elif "mute" in command:
                adjust_volume("mute")
            elif "increase brightness" in command:
                adjust_brightness("increase")
            elif "decrease brightness" in command:
                adjust_brightness("decrease")
            elif "stop" in command or "exit" in command or "goodbye" in command:
                speak("Goodbye! Returning to home page.")
                os.system("taskkill /IM code.exe /F")
                return
            else:
                speak("I'm not sure about that. Let me search it for you.")
                webbrowser.open(f"https://www.google.com/search?q={command}")

if __name__ == "__main__":
    run_veronika()
