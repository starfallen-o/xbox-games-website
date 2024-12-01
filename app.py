from flask import Flask, render_template
from flask_cors import CORS
import os
import config

# Blueprints
from blueprints.games.games import games_bp
from blueprints.media.media import media_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(games_bp)
app.register_blueprint(media_bp)

@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

@app.route('/games', methods=['GET'])
def games():
    return render_template('/games.html')

@app.route('/games/<game_id>', methods=['GET'])
def game_details(game_id):
    return render_template('/game_details.html', game_id=game_id)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
