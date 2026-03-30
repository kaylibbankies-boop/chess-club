"""
Chess Club Routes (URL Configuration)
Not needed in Flask as routes are defined as blueprints in views.py

To register the blueprint in your Flask app, add this to your main app file:
    
    from chess_club.views import chess_bp
    app.register_blueprint(chess_bp)

Available endpoints:
    GET|POST   /api/chess/members
    GET        /api/chess/members/<id>
    PATCH|PUT  /api/chess/members/<id>
    DELETE     /api/chess/members/<id>
    GET        /api/chess/members/leaderboard
    GET        /api/chess/members/<id>/public-profile
    GET        /api/chess/members/search?q=query
    
    GET|POST   /api/chess/matches
    GET        /api/chess/matches/recent
    POST       /api/chess/matches/record
    GET        /api/chess/matches/<id>
"""
