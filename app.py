from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Connect
import os

app = Flask(__name__)

@app.route("/voice", methods=["POST"])
def voice():
    """Twilio will call this endpoint when someone calls your Twilio number."""
    resp = VoiceResponse()

    # Connect to OpenAI Realtime API (AI voice)
    connect = Connect()
    connect.stream(
        url="wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview"
    )
    resp.append(connect)
    return Response(str(resp), mimetype="text/xml")

@app.route("/")
def index():
    return "AI Voice Assistant Ready!"

if __name__ == "__main__":
    app.run(port=5000)
