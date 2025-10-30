from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Voice Assistant Ready!"

# Optional test route to verify it's working
@app.route("/test")
def test():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
