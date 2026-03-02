from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://jsonplaceholder.typicode.com/todos"
cached_data = None  # simple in-memory cache


def fetch_data():
    global cached_data
    if cached_data is not None:
        return cached_data

    try:
        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()
        cached_data = response.json()
        return cached_data
    except requests.RequestException:
        return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    # Validation
    if not user_input:
        return jsonify({"reply": "🙂 Please enter a user ID so I can help you."})

    if not user_input.isdigit():
        return jsonify({
            "reply": "⚠️ Oops! That doesn't look like a valid number.\n"
                 "Please enter a user ID between 1 and 10 (example: 1)."
    })
    user_id = int(user_input)

    data = fetch_data()
    if data is None:
        return jsonify({"reply": "🌐 I'm having trouble connecting right now.\n"
                         "Please try again in a moment."})
    try:
        user_todos = [todo for todo in data if todo["userId"] == user_id]

        if not user_todos:
            return jsonify({"reply": f"🤔 I couldn’t find any records for user ID {user_id}.\n"
                         "Try a number between 1 and 10."})
        total = len(user_todos)
        completed = sum(1 for t in user_todos if t["completed"])
        pending = total - completed
        percentage = (completed / total) * 100

        first_five = user_todos[:5]
        titles = "\n".join([f"- {t['title']}" for t in first_five])

        reply = (
            f"Total: {total}\n"
            f"Completed: {completed}\n"
            f"Pending: {pending}\n"
            f"Completion: {percentage:.2f}%\n\n"
            f"First 5 titles:\n{titles}"
        )

        return jsonify({"reply": reply})

    except Exception:
        return jsonify({"reply": "Unexpected error while processing data."})


if __name__ == "__main__":
    app.run(debug=True)
