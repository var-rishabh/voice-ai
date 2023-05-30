import speech_recognition as sr
import openai
from datetime import datetime
import win32com.client

protonChat = ""
apikey = "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"


def chat(query):
    global protonChat

    openai.api_key = apikey

    protonChat += f"Rishabh: {query} \nProton: "

    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = protonChat,
        temperature = 0.7,
        max_tokens = 256,
        top_p = 1,
        frequency_penalty = 0,
        presence_penalty = 0
    )

    print("Proton:", response["choices"][0]["text"])
    say(response["choices"][0]["text"])

    protonChat += f"{response['choices'][0]['text']}\n"
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
            print("Proton: Recognizing... ")
            query = speech_input.recognize_google(audio, language="en-in")
            print(f"You: {query}")
            return query
        except Exception as e:
            return "Proton: Sorry, I didn't get it. System Error."


if _name_ == '_main_':
    print('Proton: Hey! I am Proton. Your A I Robot.')
    say('Hey! I am Proton. Your A I Robot.')
    print('Proton: How can I help you?')
    say('How can I help you?')

    while True:
        print("Proton: Listening ... ")

        query = takeInput()

        if "tell the time" in query.lower():
            current_time = datetime.today().strftime("%I:%M %p")
            print(f"Proton: Time is {current_time}")
            say(f"Time is {current_time}")

        elif "proton stop" in query.lower():
            print("Proton: Ok! Signing off.")
            say("Ok! Signing off.")
            exit()

        else:
            chat(query)
