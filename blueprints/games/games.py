from flask import Blueprint

# Blueprint
games_bp = Blueprint("games_bp", __name__)

# Get all games
@games_bp.route('/api/v1/games', methods=['GET'])

