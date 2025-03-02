from flask import Flask, request, jsonify
import grpc
import riva.client

app = Flask(__name__)

# Initialize Riva Client
RIVA_SERVER = "localhost:50051"  # Replace with actual Riva server endpoint
riva_client = riva.client.Auth(riva.client.Connection(RIVA_SERVER))

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    # Call NVIDIA Riva for NLP processing
    try:
        nlp_service = riva.client.NLPService(riva_client)
        response = nlp_service.process_text(user_input)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
