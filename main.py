import random
from flask import Flask, request, render_template
from datetime import date

app = Flask(__name__)

# List of motivational quotes
quotes = [
    "Happiness is not by chance, it’s by choice. 😊",
    "Every day may not be good, but there is something good in every day. 🌸",
    "Keep going, you’re doing great! 💪",
    "Take a deep breath and smile. 😌",
    "Your feelings are valid. 💖"
]

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    filter_mood = request.args.get("filter")
    today = date.today()

    # Random quote for this page load
    quote = random.choice(quotes)

    # Handle form submission
    if request.method == "POST":
        mood = request.form["mood"]
        note = request.form["note"]
        with open("mood_history.txt", "a") as file:
            file.write(f"{today} | Mood: {mood} | Note: {note}\n")
        message = "Your mood has been saved!"
        quote = random.choice(quotes)  # show new quote after saving

    # Read past moods
    try:
        with open("mood_history.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    # Filter moods
    if filter_mood:
        lines = [line for line in lines if f"Mood: {filter_mood}" in line]

    return render_template("index.html", moods=lines, message=message, quote=quote, today=today)

if __name__ == "__main__":
    app.run(debug=True)
