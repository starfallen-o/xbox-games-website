from flask import Blueprint, request, jsonify
from azure.cosmos import exceptions
from azure.storage.blob import ContentSettings
import uuid
import urllib.parse
import config

# Blueprint
media_bp = Blueprint("media_bp", __name__)

# CosmosDB Container
games_container = config.games_container
blob_container_client = config.blob_container_client


# Upload a new media file
@media_bp.route('/api/v1/games/<game_id>', methods=['POST'])
def upload_media(game_id):
    game_id = request.form.get('gameId')
    file = request.files.get('mediaFile')
    file_type = file.content_type or "application/octet-stream"

    if not game_id or not file:
        return jsonify({"message": "Game ID and media file are required."}), 400
    
    try:
        file_name = f"{uuid.uuid4()}_{file.filename}"
        blob_client = blob_container_client.get_blob_client(file_name)
        blob_client.upload_blob(file, 
                                overwrite=True,
                                content_settings = ContentSettings(content_type=file_type)
                                )

        media_url = f"{blob_client.url}"

        game = games_container.read_item(item=game_id, partition_key=game_id)

        if "media" not in game:
            game["media"] = []
        game["media"].append(media_url)

        games_container.upsert_item(game)

        return jsonify({"message" : "Media file uploaded successfully"}), 200
    except exceptions.CosmosResourceNotFoundError:
        return jsonify({"error" : "Game not found"}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error" : "Failed to upload media"}), 500
    

# Delete a media file
@media_bp.route('/api/v1/games/<game_id>/media', methods=['DELETE'])
def delete_media(game_id):
    data = request.get_json()
    media_url = data.get("media_url")

    if not media_url:
        return jsonify({"error": "Media URL is required"}), 400

    try:
        game = games_container.read_item(item=game_id, partition_key=game_id)

        if media_url in game["media"]:
            game["media"].remove(media_url)

            games_container.replace_item(item=game_id, body=game)

            blob_name = media_url.split('/')[-1]
            blob_name = urllib.parse.unquote(blob_name)
            blob_client = blob_container_client.get_blob_client(blob_name)
            blob_client.delete_blob()

            return jsonify({"message": "Media deleted successfully"}), 200
        else:
            return jsonify({"error": "Media not found"}), 404
    except exceptions.CosmosResourceNotFoundError as error:
        print("Error: Game not found")
        print(f"CRNF error details: {error}")
        return jsonify({"error": "Game not found"}), 404
    except Exception as e:
        print(f" 500 error details: {e}")
        return jsonify({"error": str(e)}), 500