from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Routes for each section
@app.route('/wikiRuf')
def wikiRuf():
    return render_template('wikiRuf.html')

@app.route('/RuffyWeather')
def ruffyWeather():
    return render_template('RuffyWeather.html')

@app.route('/newsR')
def newsR():
    return render_template('newsR.html')

@app.route('/stackY')
def stackY():
    return render_template('stackY.html')

# Set CORS headers for all routes
@app.after_request
def set_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, PUT, PATCH, DELETE'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

# Route for handling Wikipedia API requests
@app.route('/get_wikipedia_data')
def get_wikipedia_data():
    query = request.args.get('query')
    wikipedia_api_url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&titles={query}&redirects=1'

    # Forward the request to Wikipedia API
    response = requests.get(wikipedia_api_url)

    return jsonify(response.json()), 200

# Route for handling Stack Overflow API requests
@app.route('/get_stack_overflow_data')
def get_stack_overflow_data():
    query = request.args.get('query', '')
    stack_overflow_api_url = f'https://api.stackexchange.com/2.3/search?order=desc&sort=activity&intitle={query}&site=stackoverflow'

    try:
        response = requests.get(stack_overflow_api_url)
        data = response.json()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for handling news requests using News API
@app.route('/get_news_data')
def get_news_data():
    query = request.args.get('query')
    news_api_key = 'YOUR_NEWS_API_KEY'  # Replace with your News API key
    news_api_url = f'https://newsapi.org/v2/everything?q={query}&apiKey={news_api_key}'

    try:
        response = requests.get(news_api_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        if 'articles' in data:
            return jsonify({'articles': data['articles']}), 200
        else:
            return jsonify({'error': 'No articles found for the query'}), 404
    except requests.RequestException as e:
        app.logger.error(f"Error fetching data from News API: {e}")
        return jsonify({'error': f'Error fetching data from News API: {e}'}), 500

# Route for handling weather requests using MetaWeather API
@app.route('/get_weather')
def get_weather():
    city = request.args.get('city', 'Karachi')  # Default city is Karachi
    meta_weather_api_url = f'https://www.metaweather.com/api/location/search/?query={city}'

    try:
        response = requests.get(meta_weather_api_url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        woeid = data[0]['woeid'] if data else None

        if woeid:
            weather_url = f'https://www.metaweather.com/api/location/{woeid}/'
            weather_response = requests.get(weather_url)
            weather_response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            weather_data = weather_response.json()
            if 'consolidated_weather' in weather_data and weather_data['consolidated_weather']:
                weather_description = weather_data['consolidated_weather'][0]['weather_state_name']
                return jsonify({'city': city, 'weather': weather_description}), 200
            else:
                return jsonify({'error': 'Weather data not found for the city'}), 404
        else:
            return jsonify({'error': 'City not found'}), 404
    except requests.RequestException as e:
        app.logger.error(f"Error fetching data from MetaWeather API: {e}")
        return jsonify({'error': f'Error fetching data from MetaWeather API: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
