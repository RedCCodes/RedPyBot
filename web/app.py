from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from bot.utils import load_config, save_config

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_config = {
            "BOT_TOKEN": load_config().get("BOT_TOKEN"), # Preserve the token
            "TEXT_CHANNEL_ID": request.form.get('text_channel_id'),
            "VOICE_CHANNEL_ID": request.form.get('voice_channel_id'),
            "VOLUME": float(request.form.get('volume'))
        }
        save_config(new_config)
        return redirect(url_for('index'))

    config = load_config()
    return render_template('index.html', config=config)

@app.route('/api/config', methods=['GET'])
def api_config():
    config = load_config()
    return jsonify(config)

def run_web_server():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_web_server()
