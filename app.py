from flask import Flask, render_template
import os
import config

app = Flask(__name__)

secret_value = config.secret_value

@app.route('/', methods=['GET'])
def index():
    return render_template('/html/index.html', name=secret_value)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
