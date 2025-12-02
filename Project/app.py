from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, AOFAGroupProject! Your Python project is deployed successfully."

if __name__ == "__main__":
    # Only used if running locally
    app.run(host="0.0.0.0", port=8000, debug=True)
