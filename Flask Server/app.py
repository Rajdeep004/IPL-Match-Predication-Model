from flask import Flask, request, jsonify
from flask_cors import CORS
import awsgi
import pandas as pd
import pickle

app = Flask(__name__)
CORS(app)
# Load the trained model
model = pickle.load(open('pipe.pkl', 'rb'))

@app.route('/health', methods=['GET'])
def health():
	return "Server is up and running"

@app.route('/predict', methods=['POST'])
def predict():
	data = request.get_json()
	df = pd.DataFrame(data)

	prediction = model.predict(df)

	prediction = prediction.tolist()
	if prediction[0] == 1:
		return jsonify({"predicted_winner": data["batting_team"]})
	else:
		return jsonify({"predicted_winner": data["bowling_team"]})

def lambda_handler(event, context):
	return awsgi.response(app, event, context, base64_content_types={"image/png"})
if __name__ == '__main__':
	app.run(host='localhost', port=8000)
