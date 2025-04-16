import os
from flask import Flask, request, jsonify, render_template
from google.cloud import dialogflow_v2 as dialogflow

# Initialize Flask app
app = Flask(__name__)

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your Dialogflow service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = {
  "type": "service_account",
  "project_id": "college-xolw",
  "private_key_id": "7e7511f792cd9d186ca7ba859c6965e3a81caf78",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzLLMXS79Wofcd\no0rpUS4Psx6Eo/hsROjAEp2afslfgL0Ed+K1Vss1oereJyHVd3YMC7ZsG3V64G/E\n7GTOeCDjMI3HKam2HRvc++MZJP1bXqMLLS6SOOGwvb+cQeL32PCag0ZEbJUW5Xfn\n9mbD3Cy/fS3yGAcNnvXuofys0siz9JhW7XdzcGwUmRqIM+5xEjztDyb6NXsUMT5w\nNPF7oxhAdp/CP+dqTANswp/ZKvoU73dt0o1aHppIMWkIRGVJ+nt2erPvGfnKEhwX\n+GJvY3pMUOZoNw1bCsL/S24C8YVXbMkU9I0b5c/vZfkzvWagnSwUUvwfKLCRhX6p\neLI0ajFrAgMBAAECggEAGqgpfkDIbG+CYB1y6rgniIcXS5fy63YWbrprn5hXW2cV\njWb3YA/+rFxfoMI6WBOtiL3sBl97dgGS1L3FgwD/sO1WBUM0kEylCuv1betBP75v\ntseiaHd1VHdBMlKMcwq1Q+Jd/5YWrvu1gC76O7ozyiAp8se9B5DBJB9jg/mENLQ3\ny2A8nYkmNFNtpj+UqcSi27fj9TVXYQFvRTRtqY5KcCw3MFh7ahxiHeOSLZ6GaCAc\nmL24FSHAV3GwsLkCG0+0w9OP7tvqzMX49w10UgMJQKcCYbfT/mBvWXb15GAI9xmy\nqjaqQ+zNSZ0itaKYaarzsdMB/7VDeXPm4R9JBV1cEQKBgQDfjQiz+6TqXLIBFDP4\nuXUfP4DUsnO/zbyhzPvaF/udyh1iqQ7HMWKsk6EU5BqJZZb+TvQ9hShrIrmkU37M\nGnAgKQsipebvhRwL8KeLJC0Owc1qxWbMLloJCJSkwvZ7YKt2M2Il35My76bmwN9k\nbrpKAYcU0+GRKGBcLCRxxXAdkwKBgQDNLq3PnNs9lyDEFCTH+JIdrWnsGZm4YMS4\nDI8tjKGtEh03wza3QTRsjeiOzZesQlYrgSAxCb+T6O44kdMviuogQeIwGmy7gJEy\nQAUcPL7ESvol8fWopGU9gaimu4y7Bwrc5CUfvm88JiWnEdYaumWHnsx334Sv5LzE\n41YRfTTDyQKBgQCIp3AQhd3UHgH6Qt1aSBRem7UnUEcNkriit+mk8lAvrqOz8eBE\nx92n3T70xFOsdduNbbpD+SgyBbIxz5CNOAQexLg33+6BsH7qlZv1pJGemb32bOFg\nI12KdCJZbYy68ucdhF+VA0y6MGF4YaKthDqAjtqCUttqnqH49kr4+VaF3QKBgAcw\nM3aqkCPAP62e5wr6cmQHx0Y2P2RuP3YTOpDl9GQT1mI1vJz+8885yYP3P/ERAePU\nSkRtiwCrkGz67uMjgsBOjpYQ1u5aurt/8q3ikuxdlBXwPCMEX2egO0BcIboLrR3A\nAGz0RwFcdMU9orqc/SGbNp6cfhGLefGL5WAHeunBAoGAdnEbWWDjqzynSMddxzQh\np1ogGsOriTfgPwPA18sZVaXKb8YdkSMn8eBlS2z2FQnHChKt6dBJUYxwEv9mvOIx\nKZgr5j7o9Qsp2MX7tYvmRaxpYPIRv8hRMz8WU/NjQJJ1QtHmDO5tlSBwFXD8spM7\nCz+eHAbq1iZC8cc9BLxoUYg=\n-----END PRIVATE KEY-----\n",
  "client_email": "dialogflow-service-account@college-xolw.iam.gserviceaccount.com",
  "client_id": "107056422019067360243",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dialogflow-service-account%40college-xolw.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


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

if __name__ == "__main__":
    app.run(debug=True)

