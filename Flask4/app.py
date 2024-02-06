from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(debug=True)
