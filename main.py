from elevenlabs import generate, stream, voices, play
from elevenlabs import set_api_key
import speech_recognition as sr # Speech recognition
import sqlite3

# OPENAI API KEY
set_api_key("")

from openai import OpenAI

def get_openai_response(message):
    client = OpenAI(
        api_key=""  # API KEY
    )
#f" PLACEHOLDER {message}")

    # Add instructions to the message
    instructed_message = (f" INSERT INSTRUCTIONS HERE{message}")

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": instructed_message},
        ],
        model="gpt-4-1106-preview", # Model can be freely interchanged
    )

    # Extract and return the response content
    response_text = chat_completion.choices[0].message.content
    return response_text
def transcribe_speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening ... ")
        # Adjust the recognizer sensitivity to ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        try:

            text = recognizer.recognize_google(audio, language="en-US")
            return text
        except sr.UnknownValueError:
            return "Sorry, voice was not recognized. Please try again."
        except sr.RequestError:
            return "Sorry, there was a problem with the request. Please try again."


if __name__ == '__main__':

    conn = sqlite3.connect('conversation.db') # Connection to SQL DB

    conn.execute('''CREATE TABLE IF NOT EXISTS conversations
                (id INTEGER PRIMARY KEY,
                user_id TEXT,
                user_message TEXT,
                bot_response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')


    while True:

        user_input = input("Enter your message: ")

        # Usage of voice recording code
        #spoken_text = transcribe_speech()
        #print(f"You said: {spoken_text}")


        #if spoken_text.lower() == "bye":
            #break


        response = get_openai_response(user_input)
        print(response)

        conn.execute("INSERT INTO conversations ("
                     "user_id, "
                     "user_message,"
                     "bot_response)"
                     "VALUES (?,?,?)",
                     ('user123', user_input, response))
        conn.commit()


        audio = generate(
            text=response,
            voice="Josh",  # Can be changed using API documentation from ElevenLabs
            model="eleven_multilingual_v2"
        )

        play(audio)





conn.close() # Close connection to SQL DB
