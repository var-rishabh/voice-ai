import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import requests
import json
import openai

openai.api_key = os.getenv('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')

# Set up text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)
conversation = ""
user_name = "User"
bot_name = "Bot"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def process_command(command):
    if "joke" in command:
        # Tell a joke
        joke = get_joke()
        print(bot_name + ": " + joke)
        speak(joke)
    elif "search" in command:
        # Perform a Google search
        query = command.replace("search", "").strip()
        search_google(query)
    elif "play" in command:
        # Play a YouTube video
        query = command.replace("play", "").strip()
        play_youtube(query)
    elif "information" in command:
        # Get information from Wikipedia
        query = command.replace("information", "").strip()
        get_wikipedia_info(query)
    else:
        # Use OpenAI for conversation
        get_openai_response(command)


def get_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = json.loads(response.text)
    joke = data["setup"] + " " + data["punchline"]
    return joke


def search_google(query):
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)


def play_youtube(query):
    url = "https://www.youtube.com/results?search_query=" + query
    webbrowser.open(url)


def get_wikipedia_info(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": "",
        "explaintext": "",
        "titles": query
    }
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    pages = data["query"]["pages"]
    for page_id in pages:
        page = pages[page_id]
        if "extract" in page:
            info = page["extract"]
            print(bot_name + ": " + info)
            speak(info)
            return


def get_openai_response(command):
    global conversation
    prompt = user_name + ": " + command + "\n" + bot_name + ": " + conversation

    if "hello" in command or "hi" in command:
        response_str = "Hello! How can I assist you today?"
    else:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response_str = response.choices[0].text.strip()

    conversation += "\n" + command + "\n" + response_str
    print(bot_name + ": " + response_str)
    speak(response_str)


while True:
    with mic as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("No longer listening")
    try:
        user_input = r.recognize_google(audio)
        process_command(user_input.lower())
    except:
        continue
