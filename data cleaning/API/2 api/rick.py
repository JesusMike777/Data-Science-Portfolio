from flask import Flask, jsonify, render_template
import requests

app= Flask(__name__)

def get_data(endpoint):    
    data = requests.get(f'https://rickandmortyapi.com/api/{endpoint}').json()   
    return data

@app.route('/')
def index():
    return render_template('indexrick.html')

@app.route('/characters/', defaults={'character_id': None})
@app.route('/characters/<int:character_id>')
def get_characters(character_id):
    if character_id is None:
        return jsonify(get_data('character'))
    else:
        return jsonify(get_data(f'character/{character_id}'))
    

@app.route('/locations/', defaults={'location_id': None})
@app.route('/locations/<int:location_id>')
def get_locations(location_id):
    if location_id is None:
        return jsonify(get_data('location'))
    else:
        return jsonify(get_data(f'location/{location_id}'))

@app.route('/episodes/', defaults={'episode_id': None})
@app.route('/episodes/<int:episode_id>')
def get_episodes(episode_id):
    if episode_id is None:
        return jsonify(get_data('episode'))
    else:
        return jsonify(get_data(f'episode/{episode_id}'))

app.run(debug=True, host='localhost', port=5000)