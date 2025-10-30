from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
import openai, os

app = Flask(__name__)

# --- Load OpenAI Key ---
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "✅ AI Voice Assistant Ready!"

@app.route("/voice", methods=["POST"])
def voice():
    # Get the caller’s speech (if any)
    caller_number = request.form.get("From", "")
    recording_url = request.form.get("RecordingUrl", "")
    user_input = request.form.get("SpeechResult", "")

    print(f"📞 Call from: {caller_number}")
    print(f"💬 User said: {user_input}")

    # Generate AI reply using OpenAI
    prompt = f"The user said: {user_input}. Reply naturally like an assistant that can understand any language."

    ai_reply = "Hello, how can I help you?"  # default fallback
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_reply = completion.choices[0].message["content"]
    except Exception as e:
        print(f"❌ OpenAI error: {e}")

    # Twilio Voice response
    resp = VoiceResponse()
    resp.say(ai_reply, voice="Polly.Amy", language="en-US")  # Polly.Amy is natural female voice

    # Optionally record call
    resp.record(maxLength="30", playBeep=True)

    return Response(str(resp), mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
