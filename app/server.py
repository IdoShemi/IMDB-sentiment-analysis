from flask import Flask, request, request, render_template
from predict import predict_sentiments
from imdb_reviews import get_movie_reviews # change
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

def get_movie(movie_link):
    if not movie_link:
        return {"error": "movie_id is required"}

    comments = get_movie_reviews(movie_link)
    predictions = predict_sentiments(comments)

    positive = predictions.count("Positive")
    negative = predictions.count("Negative")

    summary = {
        "positive": positive,
        "negative": negative,
        "num_comments": len(comments),
        "rating": (positive / len(comments)) * 100
    }

    return {"predictions": predictions, "comments": comments, "summary": summary}


@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    comments = []
    if request.method == 'POST':
        movie_url = request.form.get('movie_url')
        data = get_movie(movie_url)

        summary = data['summary']
        comments = list(zip(data['comments'], data['predictions']))
    return render_template('index.html', summary=summary, comments=comments)

if __name__ == '__main__':
    import webbrowser
    webbrowser.open('http://127.0.0.1:5000/')

    app.run(debug=True)
