from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/voice", methods=["POST"])
def voice():
    user_input = request.values.get("SpeechResult", "").strip()
    print(f"User said: {user_input}")

    # Detect language (basic logic)
    if any(word in user_input.lower() for word in ["hai", "mujhe", "bukhar", "dard", "nahi", "kya"]):
        language = "hindi"
    else:
        language = "english"

    # Multilingual prompt
    if language == "hindi":
        prompt = f"Respond in Hindi in one short sentence: {user_input}"
    else:
        prompt = f"Respond in English in one short sentence: {user_input}"

    # Generate AI response
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a friendly AI medical assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    ai_reply = completion.choices[0].message.content
    print("AI Reply:", ai_reply)

    # Twilio voice response
    response = VoiceResponse()
    response.say(ai_reply, language="hi-IN" if language == "hindi" else "en-US")

    return str(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
