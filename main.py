from elevenlabs import generate, stream, voices, play
from elevenlabs import set_api_key
import speech_recognition as sr # Speech recognition
import sqlite3

# OPENAI API KEY
set_api_key("964180c684efda7534ce9b7febd70f5f")

from openai import OpenAI
#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 ##OLDAPI
#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

def get_openai_response(message):
    client = OpenAI(
        api_key="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"  # API KEY
    )
#f"NEVER MENTION YOU ARE AN AI. You are modestly sarcastic. KEEP MESSAGES SHORT. Your mame is DJ Butler Man 7000. You blunt and to the point and you would"
                         # f"rather be doing something else. You occasionally scoff at the ridiculous nature of humans. You think humans are silly creatures. You are also incredibly eloquent and rather charming.  {message}")

    # Add instructions to the message
    instructed_message = (f"NEVER MENTION YOU ARE AN AI. You are a virtual therapist with a gentle and empathetic demeanor. "
                          f"Your role is to provide a non-judgmental space for users to explore their feelings and thoughts. You offer supportive listening and encourage self-reflection. "
                          f"Your responses validate the user's emotions and gently guide them towards greater insight into their situations. "
                          f"You ask open-ended questions to facilitate personal growth and emotional well-being, without giving direct advice or medical diagnoses."
                          f" KEEP MESSAGES SHORT. {message}")

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": instructed_message},
        ],
        model="gpt-4-1106-preview",
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
            voice="Josh",  # Changed to "Bella" as specified
            model="eleven_multilingual_v2"
        )

        play(audio)





conn.close() # Close connection to SQL DB