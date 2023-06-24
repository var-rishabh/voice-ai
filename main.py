from datetime import datetime
import pyttsx3
import webbrowser
import os
import requests
import json
import openai
import speech_recognition as sr
import win32com.client

optimusChat = ""
apikey = ""


def processCommand(query):
    if "tell the time" in query:
        current_time = datetime.today().strftime("%I:%M %p")
        print(f"Optimus: Time is {current_time}")
        say(f"Time is {current_time}")
            
    elif "tell a joke" in query:
        joke = get_joke()
        print(f"Optimus: {joke}")
        say(joke)
            
    elif "search" in query:
        query = query.split("search", 1)[1]
        print(f"Optimus: {query}")
        say("Searching on google")
        url = "https://www.google.com/search?q=" + query
        webbrowser.open(url)
            
    elif "play" in query:
        query = query.split("play", 1)[1]
        print(f"Optimus: {query}")
        say("Playing on youtube")
        url = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(url)

    elif "optimus quit" in query:
        print("Optimus: Ok! Signing off.")
        say("Ok! Signing off.")
        return "quit"

    else:
        chat(query)

def get_joke():
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    data = json.loads(response.text)
    joke = data["setup"] + " " + data["punchline"]
    return joke

def chat(query):
    global optimusChat
    openai.api_key = apikey
    optimusChat += f"Rishabh: {query} \nOptimus: "
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = optimusChat,
        temperature = 0.7,
        max_tokens = 256,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )

    print("Optimus:", response["choices"][0]["text"])
    say(response["choices"][0]["text"])
    
    optimusChat += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)


def takeInput():
    speech_input = sr.Recognizer()
    with sr.Microphone() as source:
        speech_input.pause_threshold = 0.8
        audio = speech_input.listen(source)
        try:
            print("Optimus: Recognizing... ")
            query = speech_input.recognize_google(audio, language="en-in")
            print(f"You: {query}")
            return query
        except Exception as e:
            return "Optimus: Sorry, I didn't get it. System Error."


if __name__ == '__main__':
    print('Optimus: Hey! I am Optimus. Your A.I. Bot.')
    say('Hey! I am Optimus. Your A I Bot.')
    print('Optimus: How can I help you?')
    say('How can I help you?')

    while True:
        try:
            print("Optimus: Listening ... ")
            query = takeInput()
            ans = processCommand(query.lower())
            if (ans == "quit") :
                break
        except: 
            continue
