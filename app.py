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
def chatbot_response(user_message):
    msg = user_message.lower()

    # Greeting
    if msg in ["hi", "hello", "hey"]:
        return "Hello! 👋 Welcome to Nimbus Support. How can I assist you today?"

    # Help
    elif "help" in msg:
        return """Sure! I'm here to help 😊
1️⃣ Account Issues
2️⃣ Order Status
3️⃣ Technical Support
4️⃣ Talk to a Human Agent"""

    # Order status
    elif "order" in msg:
        return "📦 Please enter your **Order ID** to check the latest order status."

    # Login issue
    elif "login" in msg:
        return """No worries! 🔐
You can reset your password using the **Forgot Password** option.
Would you like me to send the reset link?"""

    # OTP issue
    elif "otp" in msg:
        return """Sometimes OTPs take a few seconds ⏳
Please wait **30 seconds** and try again.
Would you like me to resend the OTP?"""

    # Services info
    elif "services" in msg:
        return """We offer several services:
✅ AI Automation
✅ Data Analytics
✅ Chatbot Development
✅ Dashboard & Reporting

Would you like more details about any of these?"""

    # Demo request
    elif "demo" in msg:
        return """Great! 🚀
Please share your **name, email, and company name**.
Our team will schedule a **free demo** for you."""

    # Human support
    elif "human" in msg or "agent" in msg:
        return "Sure 👍 Connecting you with a support specialist. Please wait…"

    # Thanks
    elif "thank" in msg:
        return "You're welcome! 😊 If you need anything else, feel free to ask."

    # Goodbye
    elif "bye" in msg:
        return "Thank you for visiting! 👋 Have a wonderful day."

    # Default response
    else:
        return """I'm sorry, I didn't understand that. 🤔
Please choose:
1️⃣ Account Issues
2️⃣ Order Status
3️⃣ Technical Support
4️⃣ Talk to a Human Agent"""   


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()

    # If input is NOT a number → chatbot responses
    if not user_input.isdigit():
        bot_reply = chatbot_response(user_input)
        if bot_reply:
            return jsonify({"reply": bot_reply})

        return jsonify({
            "reply": "🙂 Please enter a user ID between 1 and 10."
        })

    # If input is a number → run API logic
    user_id = int(user_input)

    # Validation
    if not user_input:
        return jsonify({"reply": "🙂 Please enter a user ID so I can help you."})

    if not user_input.isdigit():
        return jsonify({
            "reply": "Hello! I'm not quite able to process that just yet. Would you mind entering a user ID between 1 and 10 instead?"
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


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
