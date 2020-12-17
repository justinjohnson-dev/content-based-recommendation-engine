from flask import Flask
from reccomendation_engine import get_recommendation
app = Flask(__name__)

@app.route('/')
def index():
    get_recommendation()
    return 'Web App with Python Flask!'

app.run(host='0.0.0.0', port=81)