from flask import Flask
from projects.main import main  # Adjust if your main.py is in a subfolder like 'projects/'

app = Flask(__name__)

@app.route("/")
def home():
    return "AOFAGroupProject is deployed! Your CLI logic runs locally."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)  # Azure will map the port
