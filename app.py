from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)  # allows React frontend to call the API

analyzer = SentimentIntensityAnalyzer()

@app.route('/')
def home():
    return jsonify({
        "message": "Sentiment Analysis API",
        "endpoints": {
            "/sentiment": "POST - Analyze sentiment of text"
        },
        "example_usage": {
            "method": "POST",
            "url": "/sentiment",
            "body": {"sentence": "Your text here"}
        }
    })

@app.route('/sentiment', methods=['POST'])
def sentiment_score():
    data = request.get_json()
    sentence = data.get("sentence", "")

    sentiment_dict = analyzer.polarity_scores(sentence)

    if sentiment_dict["compound"] >= 0.05:
        sentiment = "Positive"
    elif sentiment_dict["compound"] <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    response = {
        "sentence": sentence,
        "sentiment": sentiment,
        "scores": sentiment_dict
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)