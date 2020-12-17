from flask import Flask, request

from reccomendation_engine import get_recommendation
app = Flask(__name__)

# http://localhost:81/?movie=The%20Dark%20Knight%20Rises
@app.route('/')
def index():
    # Error trapping is for noobs.
    movie_recommendations = get_recommendation(request.args.get('movie'))
    return movie_recommendations.to_json()

app.run(host='0.0.0.0', port=81)