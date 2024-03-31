import speech_recognition as sr
import pyttsx3
from transformers import pipeline

import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

tts_engine = pyttsx3.init()

with open('information.txt', 'r') as file:
    hotel_info = file.read()

context = f"""

You are recepcionist in a hotel. You have to answer questions from customers. Here is some information about the hotel:
{hotel_info}

You will now be asked a question by a customer, please answer shortly.
"""

hardcoded_triggers = {
    "hello": "Hello! Welcome to the Grand Sofia Hotel. How can I assist you today?",
    "check in": "To check in, please provide your reservation details.",
    "check out": "Hope you had a pleasant stay! Your check-out has been processed."
}

trigger_variations = {
    "hello": ["hello", "hi", "hey", "greetings"],
    "check in": ["check in", "want to check in", "checking in", "i'd like to check in"],
    "check out": ["check out", "checking out", "i want to check out", "i'd like to check out"]
}

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def check_for_triggers(question):
    for trigger, variations in trigger_variations.items():
        for variation in variations:
            if variation in question.lower():
                return hardcoded_triggers[trigger]
    return None

def recognize_speech_from_mic(recognizer, microphone):
    print("Listening for your question...")
    with microphone as source:
        try:
            audio_data = recognizer.listen(source, timeout=10)
        except sr.WaitTimeoutError:
            print("Timeout error: No speech detected within the timeout limit.")
            return ""

        try:
            print(recognizer.recognize_google(audio_data))
            return recognizer.recognize_google(audio_data)
        except (sr.UnknownValueError, sr.RequestError):
            return ""



def get_answer_from_context(question):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": question
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        question_from_speech = recognize_speech_from_mic(recognizer, microphone)
        if question_from_speech:
            if "goodbye" in question_from_speech.lower():
                goodbye_message = "Goodbye! Have a great day."
                print(goodbye_message)
                speak(goodbye_message)
                break

            response = check_for_triggers(question_from_speech)
            if response:
                print(f"Response: {response}")
                speak(response)
            else:
                answer = get_answer_from_context(question_from_speech)
                print(f"Answer: {answer}")
                speak(answer)

if __name__ == "__main__":
    main()
