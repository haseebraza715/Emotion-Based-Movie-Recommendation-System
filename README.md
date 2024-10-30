# Emotion-Based Movie Recommendation System

This project is an **Emotion-Based Movie Recommendation System** built with Python and Flask. It recommends movies based on their emotional impact by analyzing user reviews. Using natural language processing (NLP), the system categorizes movies into emotional types like "uplifting," "intense," "dark," "thought-provoking," "romantic," and "humorous."

## Features
- **Emotion-Centric Recommendations**: Recommends movies based on emotional categories.
- **Sentiment Analysis**: Analyzes movie reviews using VADER and TextBlob to determine sentiment and subjectivity.
- **Responsive Web Interface**: Built with Flask, HTML, and CSS.

## Requirements
- **Python 3.6+**
- **Libraries**:
  - `Flask`
  - `Requests`
  - `Dotenv`
  - `NLTK` and `VADER Sentiment Analysis`
  - `TextBlob`
  - `Numpy`
- **TMDb API Key**: Sign up for an API key [here](https://www.themoviedb.org/).

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/emotion-based-movie-recommender.git
   cd emotion-based-movie-recommender
   ```

2. Install the required libraries:
   ```bash
   pip install Flask requests python-dotenv nltk textblob numpy
   ```

3. Set up your **TMDb API key**:
   - Create a `.env` file and add your API key:
     ```plaintext
     TMDB_API_KEY=your_api_key_here
     ```

4. Download necessary NLTK data:
   ```python
   import nltk
   nltk.download('vader_lexicon')
   ```

## Usage
1. Run the Flask app:
   ```bash
   python app.py
   ```
2. Open your browser and go to `http://127.0.0.1:5000`.
3. Choose an emotion to receive movie recommendations based on that emotional category.

## Project Structure
- `app.py`: Main application logic.
- `templates/`: HTML templates for the web interface.
- `static/style.css`: Styling for the web app.

## Future Improvements
- Integrate advanced models like BERT for more nuanced emotion detection.
- Add user feedback to improve recommendation accuracy.
- Expand with machine learning for category classification.

## License
This project is licensed under the MIT License.

