from flask import Flask, render_template
import os
import config

# Blueprints
from blueprints.games.games import games_bp
from blueprints.auth.auth import auth_bp

app = Flask(__name__)

app.register_blueprint(games_bp)
app.register_blueprint(auth_bp)

@app.route('/', methods=['GET'])
def index():
    return render_template('/html/index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
