from flask import Blueprint, Flask, jsonify, request
from azure.cosmos import exceptions
import uuid
import config

# Blueprint
games_bp = Blueprint("games_bp", __name__)

# CosmosDB Container
games_container = config.games_container
blob_container_client = config.blob_container_client


# Show all games
@games_bp.route('/api/v1/games', methods=['GET'])
def show_all_games():
    games = list(games_container.read_all_items())
    return jsonify(games)


# Show one game
@games_bp.route('/api/v1/games/<game_id>', methods=['GET'])
def show_one_game(game_id):
    try:
        game = games_container.read_item(item=game_id, partition_key=game_id)
        return jsonify(game), 200
    except exceptions.CosmosResourceNotFoundError:
        return jsonify({"error": "Game not found"}), 404


# Upload a new game
@games_bp.route('/api/v1/games', methods=['POST'])
def upload_game():
    data = request.form

    files = request.files.getlist("files[]")
    if not files:
        return jsonify({"error": "At least one media file is required"}), 400
    
    media_urls = []

    for file in files:
        file_name = f"{uuid.uuid4()}_{file.filename}"

        blob_client = blob_container_client.get_blob_client(file_name)
        blob_client.upload_blob(file, overwrite=True)

        media_url = f"{blob_client.url}"
        media_urls.append(media_url)

    metadata = {
        "id": str(uuid.uuid4()),
        "title": data.get('title'),
        "description": data.get('description'),
        "cost": data.get('cost'),
        "release_date": data.get('release_date'),
        "genre": data.get('genre'),
        "publisher": data.get('publisher'),
        "age_rating": data.get('age_rating'),
        "media": media_urls
    }

    games_container.create_item(metadata)
    return jsonify({"message": "Game uploaded successfully", "game": metadata}), 201


# Edit an existing game
@games_bp.route('/api/v1/games/<game_id>', methods=['PUT'])
def edit_game(game_id):
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request data"}), 400
    
    title = data.get("title")
    description = data.get("description")
    cost = data.get("cost")
    release_date = data.get("release_date")
    genre = data.get("genre")
    publisher = data.get("publisher")
    age_rating = data.get("age_rating")

    try:
        game = games_container.read_item(item=game_id, partition_key=game_id)

        game["title"] = title
        game["description"] = description
        game["cost"] = cost
        game["release_date"] = release_date
        game["genre"] = genre
        game["publisher"] = publisher
        game["age_rating"] = age_rating

        games_container.upsert_item(game)

        return jsonify({"message": "Game updated successfully"}), 200
    except exceptions.CosmosResourceNotFoundError:
        return jsonify({"error": "Game not found"}), 404
    except Exception as e:
        print(f"error: {e}")
        return jsonify({"error": "Failed to update game"}), 500
    

# Delete a game and its media
@games_bp.route('/api/v1/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    try:
        game = games_container.read_item(item=game_id, partition_key=game_id)

        for media_url in game.get("media", []):
            blob_name = media_url.split('/')[-1]
            blob_client = blob_container_client.get_blob_client(blob_name)
            blob_client.delete_blob()

        games_container.delete_item(item=game_id, partition_key=game_id)

        return jsonify({"message": "Game and its media deleted successfully"}), 200
    except exceptions.CosmosResourceNotFoundError:
        return jsonify({"error": "Game not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500