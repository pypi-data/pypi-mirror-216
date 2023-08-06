import openai
import os
from Polly import Polly

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAIKEY")


# Initialisieren Sie das Gespräch
conversation = [
     
]

while True:
    # Get user input
    user_input = input("User: ")


    # Benutzereingabe zum Gespräch hinzufügen
    conversation.append({"role": "user", "content": user_input})

    # API-Aufruf durchführen
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Verwenden Sie das gewünschte Modell
        messages=conversation,
        max_tokens=50,
        temperature=0.7
    )

    # Get the assistant's reply
    reply = response['choices'][0]['message']['content']

    # Print the assistant's reply
    print("Assistant:", reply)
    synthesizer = Polly(reply)
    synthesizer.start()

    # Antwort des Assistenten zum Gespräch hinzufügen
    conversation.append({"role": "assistant", "content": reply})
