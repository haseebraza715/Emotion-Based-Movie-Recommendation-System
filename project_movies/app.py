import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import numpy as np

# Download VADER lexicon
nltk.download('vader_lexicon')

# Load environment variables
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

app = Flask(__name__)

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to get popular movies
def get_popular_movies():
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

# Function to get reviews for a specific movie
def get_movie_reviews(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/reviews"
    params = {
        "api_key": API_KEY,
        "language": "en-US",
        "page": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return [review['content'] for review in response.json().get("results", [])]
    return []

# Function to analyze and aggregate reviews
def analyze_and_aggregate_reviews(reviews):
    vader_scores, polarity_scores, subjectivity_scores = [], [], []

    for review in reviews:
        vader_score = sia.polarity_scores(review)['compound']
        vader_scores.append(vader_score)
        blob = TextBlob(review)
        polarity_scores.append(blob.sentiment.polarity)
        subjectivity_scores.append(blob.sentiment.subjectivity)

    return {
        "avg_vader_score": np.mean(vader_scores),
        "avg_polarity_score": np.mean(polarity_scores),
        "avg_subjectivity_score": np.mean(subjectivity_scores)
    }



def recommend_movies(movies, preference):
    # Calculate adaptive thresholds
    vader_scores = []
    polarity_scores = []
    subjectivity_scores = []
    for movie in movies:
        reviews = get_movie_reviews(movie['id'])
        if reviews:
            profile = analyze_and_aggregate_reviews(reviews)
            vader_scores.append(profile['avg_vader_score'])
            polarity_scores.append(profile['avg_polarity_score'])
            subjectivity_scores.append(profile['avg_subjectivity_score'])
    
    # Calculate means and adjust thresholds
    vader_threshold = np.mean(vader_scores) + 0.1  # Slightly above average for positive
    polarity_threshold = np.mean(polarity_scores) + 0.1
    subjectivity_threshold = np.mean(subjectivity_scores) + 0.1

    recommendations = []

    for movie in movies:
        reviews = get_movie_reviews(movie['id'])
        if reviews:
            profile = analyze_and_aggregate_reviews(reviews)
            avg_vader_score = profile['avg_vader_score']
            avg_polarity_score = profile['avg_polarity_score']
            avg_subjectivity_score = profile['avg_subjectivity_score']

            # Keyword-based boosts
            keywords = " ".join(reviews).lower()
            romantic_boost = keywords.count("romantic") + keywords.count("love")
            humorous_boost = keywords.count("funny") + keywords.count("comedy")

            if preference == "uplifting" and avg_vader_score > vader_threshold:
                recommendations.append((movie['title'], avg_vader_score))

            elif preference == "intense" and avg_subjectivity_score > subjectivity_threshold:
                recommendations.append((movie['title'], avg_subjectivity_score))

            elif preference == "dark" and avg_vader_score < -0.1:
                recommendations.append((movie['title'], avg_vader_score))

            elif preference == "thought-provoking" and 0.3 < avg_subjectivity_score < 0.6 and abs(avg_polarity_score) < 0.2:
                recommendations.append((movie['title'], avg_subjectivity_score))

            elif preference == "romantic" and avg_polarity_score > polarity_threshold and romantic_boost > 2:
                recommendations.append((movie['title'], avg_polarity_score))

            elif preference == "humorous" and avg_vader_score > 0.2 and humorous_boost > 1:
                recommendations.append((movie['title'], avg_vader_score))

    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return recommendations





# Flask route for the main page
@app.route('/')
def index():
    return render_template("index.html")

# Flask route to handle form submission and show recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    preference = request.form.get("preference")
    movies = get_popular_movies()
    recommendations = recommend_movies(movies, preference)
    return render_template("results.html", preference=preference.capitalize(), recommendations=recommendations)
# Additional route for "About" page
@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
