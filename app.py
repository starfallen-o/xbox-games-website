from flask import Flask, render_template
import os
import globals

# Blueprints
from blueprints.games.games import games_bp

app = Flask(__name__)

app.register_blueprint(games_bp)

secret_value = globals.secret_value

@app.route('/', methods=['GET'])
def index():
    return render_template('/html/index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4999))
    app.run(debug=True, host='0.0.0.0', port=port)