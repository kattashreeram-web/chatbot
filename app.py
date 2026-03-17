from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

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
    from datetime import datetime

    # Time-based greeting
    ist = pytz.timezone('Asia/Kolkata')
    current_hour = datetime.now(ist).hour
    if current_hour < 12:
        greeting = "Good morning ☀️"
    elif current_hour < 17:
        greeting = "Good afternoon 🌤️"
    else:
        greeting = "Good evening 🌙"

    # -------------------------
    # 🤖 NEW ZEVOIR FLOW
    # -------------------------

    # Greeting
    if any(word in msg for word in ["hi", "hello", "hey"]):
        return f"{greeting}! 👋 Welcome to Zevoir Technologies. What brings you here today?"

    # Business help
    elif "business" in msg:
        return "That’s great! 😊 Are you looking for a website, AI solution, or something else?"

    elif "ai" in msg:
        return "Awesome choice 🚀 AI can really boost efficiency. Are you thinking about automation, chatbots, or data insights?"

    # Services
    elif "services" in msg:
        return "We help businesses grow with AI, Data Analytics, Cloud, and Web & Mobile Development. What are you most interested in?"

    elif "web" in msg:
        return "Nice 👍 Are you planning a new website or upgrading an existing one?"

    elif "new website" in msg:
        return "Perfect! We can design and build a fast, modern site for you. Would you like a quick consultation?"

    # Chatbot
    elif "chatbot" in msg:
        return "Absolutely! 🤖 We create smart chatbots for customer support, automation, and sales."

    elif "work like you" in msg:
        return "Pretty close 😄 It can answer questions, guide users, and even capture leads."

    elif "sounds good" in msg:
        return "Great! Want me to connect you with our AI team for a demo?"

    # Data
    elif "data" in msg:
        return "That’s where we come in 📊 We turn raw data into clear, actionable insights."

    elif msg == "how":
        return "We build dashboards, reports, and predictive models so you can make smarter decisions."

    elif "interesting" in msg:
        return "Want to see a sample dashboard or discuss your use case?"

    # Cloud
    elif "cloud" in msg:
        return "Yes ☁️ We help businesses move to cloud platforms like AWS, Azure, and Google Cloud."

    elif "secure" in msg:
        return "Absolutely 🔐 We focus on security, scalability, and reliability."

    # Lead capture
    elif "interested" in msg:
        return "That’s great to hear! 😊 Can I have your name and email so our team can reach out?"

    elif "@" in msg:
        return "Thanks! 👍 Our team will contact you shortly."

    # Friendly
    elif "exploring" in msg:
        return "No problem at all 😊 Take your time. I’m here if you need anything!"

    elif "different" in msg:
        return "Great question! 🚀 We focus on smart solutions, fast delivery, and real business impact."

    # Closing
    elif "thanks" in msg or "thank you" in msg:
        return "You’re welcome! 😊 Let’s build something amazing together!"

    # -------------------------
    # 🧰 OLD SUPPORT LOGIC (kept)
    # -------------------------

    elif "help" in msg:
        return """Sure! I'm here to help 😊
Account Issues
Order Status
Technical Support
Talk to a Human Agent"""

    elif "order" in msg:
        return "📦 Please enter your Order ID to check the latest order status."

    elif "login" in msg:
        return """No worries! 🔐
You can reset your password using the Forgot Password option.
Would you like me to send the reset link?"""

    elif "otp" in msg:
        return """Sometimes OTPs take a few seconds ⏳
Please wait 30 seconds and try again.
Would you like me to resend the OTP?"""

    elif "demo" in msg:
        return """Great! 🚀
Please share your name, email, and company name.
Our team will schedule a free demo for you."""

    elif "human" in msg or "agent" in msg:
        return "Sure 👍 Connecting you with a support specialist. Please wait…"

    elif "bye" in msg:
        return "Thank you for visiting! 👋 Have a wonderful day."

    # Default
    else:
        return "I’m here to help 😊 Could you tell me a bit more about what you need?"
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


if __name__ == "__main__":
    app.run(debug=True)
