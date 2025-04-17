import os
from flask import Flask, request, jsonify, render_template
from google.cloud import dialogflow_v2 as dialogflow

# Initialize Flask app
app = Flask(__name__)

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your Dialogflow service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/etc/secrets/GOOGLE_APPLICATION_CREDENTIALS"




# Initialize Dialogflow Session Client
session_client = dialogflow.SessionsClient()

# Function to send user query to Dialogflow and get response
def detect_intent_texts(project_id, session_id, text, language_code='en'):
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(request={"session": session, "query_input": query_input})

    return response.query_result.fulfillment_text

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(silent=True, force=True)
    user_input = req['queryResult']['queryText']

    # Send user input to Dialogflow and get the response
    project_id = "college-xolw"  # Replace with your actual project ID
    session_id = "random-session-id"  # You can generate a unique session ID for each user interaction
    response = detect_intent_texts(project_id, session_id, user_input)

    return jsonify({'fulfillmentText': response})
# Get the port from the environment variable, or default to 5000 for local development
port = process.env.PORT

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

