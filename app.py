from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Store conversation states
user_state = {}
user_prev_state = {}  # 🔁 Track previous state

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_id = data.get('user_id')
        user_input = data.get('message').lower().strip()

        if user_id not in user_state:
            user_state[user_id] = "greeting"

        # 🔙 Handle Back button globally
        if user_input in ["⬅️ back", "back"]:
            prev = user_prev_state.get(user_id, "greeting")
            user_state[user_id] = prev
            if prev == "fee_selected":
                response_message = "💰 Which course do you want fee details for?"
                response_options = ["💻 Computer Science", "📡 Electronics", "⚙️ Mechanical", "🏠 Main Menu"]
            elif prev == "admission_selected":
                response_message = "✅ The admission process includes:\n1. Fill the online form\n2. Submit documents\n3. Attend counseling session."
                response_options = ["📄 Apply Now", "📞 Contact Admission Office", "🏠 Main Menu"]
            else:
                response_message = "🔙 You're back to the main menu. How can I help you?"
                response_options = ["📘 Admission Process", "💰 Fee Structure", "🎓 Courses Offered"]
            return jsonify({"message": response_message, "options": response_options})

        # Greeting from any state
        if "hi" in user_input or "hello" in user_input:
            user_prev_state[user_id] = user_state[user_id]
            user_state[user_id] = "waiting_for_selection"
            response_message = "👋 Hello again! How can I assist you today?"
            response_options = ["📘 Admission Process", "💰 Fee Structure", "🎓 Courses Offered"]
            return jsonify({"message": response_message, "options": response_options})

        # Main menu
        if user_state[user_id] == "greeting":
            response_message = "Hello! I’m your college assistant bot. How can I help you today?"
            response_options = ["📘 Admission Process", "💰 Fee Structure", "🎓 Courses Offered"]
            user_prev_state[user_id] = user_state[user_id]
            user_state[user_id] = "waiting_for_selection"

        elif user_state[user_id] == "waiting_for_selection":
            if "admission" in user_input:
                response_message = "✅ The admission process includes:\n1. Fill the online form\n2. Submit documents\n3. Attend counseling session."
                response_options = ["📄 Apply Now", "📞 Contact Admission Office", "⬅️ Back", "🏠 Main Menu"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "admission_selected"
            elif "fee" in user_input:
                response_message = "💰 The fee structure varies by course. Which course are you interested in?"
                response_options = ["💻 Computer Science", "📡 Electronics", "⚙️ Mechanical", "⬅️ Back", "🏠 Main Menu"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "fee_selected"
            elif "course" in user_input:
                response_message = "🎓 We offer the following courses:\n- CS (Computer Science)\n- IS (Information Science)\n- ECE (Electronics & Communication)\n- ME (Mechanical)"
                response_options = ["📘 Admission Process", "💰 Fee Structure", "⬅️ Back", "🏠 Main Menu"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "course_listed"
            else:
                response_message = "❓ I didn’t get that. Please choose one of the options below."
                response_options = ["📘 Admission Process", "💰 Fee Structure", "🎓 Courses Offered"]

        elif user_state[user_id] == "fee_selected":
            if "computer" in user_input:
                response_message = "💻 The fee for Computer Science is ₹1,25,000 per year."
                response_options = ["⬅️ Back", "🏠 Main Menu"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "greeting"
            elif "electronics" in user_input:
                response_message = "📡 The fee for Electronics & Communication is ₹1,10,000 per year."
                response_options = ["⬅️ Back", "🏠 Main Menu"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "greeting"
            elif "mechanical" in user_input:
                response_message = "⚙️ The fee for Mechanical Engineering is ₹1,00,000 per year."
                response_options = ["⬅️ Back", "🏠 Main Menu"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "greeting"
            elif "back" in user_input:
                response_message = "🔙 You're back to the main menu. How can I help you?"
                response_options = ["📘 Admission Process", "💰 Fee Structure", "🎓 Courses Offered"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "greeting"  
            elif "main" in user_input:
                response_message = "🔙 You're back to the main menu. How can I help you?"
                response_options = ["📘 Admission Process", "💰 Fee Structure", "🎓 Courses Offered"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "greeting" 
            else:
                response_message = "Please select a course to get the fee details."
                response_options = ["💻 Computer Science", "📡 Electronics", "⚙️ Mechanical", "⬅️ Back", "🏠 Main Menu"]

        elif user_state[user_id] == "admission_selected":
            if "apply" in user_input:
                response_message = "📝 You can apply online through our website. Please visit [website link]."
                response_options = ["⬅️ Back", "🏠 Main Menu"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "greeting"
            elif "contact" in user_input:
                response_message = "📞 You can contact the admission office at +91-XXXXXXXXXX or email at info@college.edu."
                response_options = ["⬅️ Back", "🏠 Main Menu"]
                user_prev_state[user_id] = user_state[user_id]
                user_state[user_id] = "greeting"
            else:
                response_message = "Please select an option to proceed."
                response_options = ["📄 Apply Now", "📞 Contact Admission Office", "⬅️ Back", "🏠 Main Menu"]

    except Exception as e:
        response_message = "❌ Error generating response."
        response_options = ["🏠 Main Menu"]

    return jsonify({
        "message": response_message,
        "options": response_options
    })


if __name__ == '__main__':
    app.run(debug=True)
