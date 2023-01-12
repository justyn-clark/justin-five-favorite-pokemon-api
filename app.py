from flask import Flask, jsonify, render_template
import requests
import random
import statistics

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/justin-five-favorite-pokemon', methods=['GET'])
def get_pokemon():
    pokemon_names = ["ditto", "golem", "exeggutor", "pikachu", "chikorita"]
    pokemon_data_list = []
    base_happiness = []
    for name in pokemon_names:
        # Make a GET request to the Pokemon endpoint
        try:
            pokemon_response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
            pokemon_response.raise_for_status()
            # Convert the response to a JSON object
            pokemon_data = pokemon_response.json()
            # Make a GET request to the Pokemon Species endpoint
            species_response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_data["id"]}')
            species_response.raise_for_status()
            # Extract the color and base_happiness from the species JSON object
            color = species_response.json()["color"]["name"]
            happiness = species_response.json()["base_happiness"]
            base_happiness.append(happiness)
            # Extract the name, height, weight, and 2 moves from the JSON object
            name = pokemon_data['name']
            height = pokemon_data['height']
            weight = pokemon_data['weight']
            moves = [move['move']['name'] for move in pokemon_data['moves']]
            # Randomize moves in list
            random.shuffle(moves)
            pokemon_data_list.append(
                {'name': name, 'height': height, 'weight': weight, 'moves': moves[:2], 'color': color,
                 'base_happiness': happiness})
        except requests.exceptions.HTTPError as err:
            # Handle any error from the GET request
            print(f"An error occurred: {err}")
    # Use statistics library to calculate average, mean, median of base_happiness
    average = sum(base_happiness) / len(base_happiness)
    mean = statistics.mean(base_happiness)
    median = statistics.median(base_happiness)
    # Return the extracted data and statistics as a JSON object
    return jsonify(pokemon_data_list=pokemon_data_list, average=average, mean=mean, median=median)
