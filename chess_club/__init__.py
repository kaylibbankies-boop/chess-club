"""
Chess Club Flask Module
A complete chess club administration app for Flask with SQLAlchemy

Available components:
- Models: ChessMember, MatchResult
- Views: Blueprint with API endpoints at /api/chess/*
- Admin (optional): Blueprint for admin routes

Usage in your Flask app:
    from chess_club.models import db, ChessMember, MatchResult
    from chess_club.views import chess_bp
    
    app.register_blueprint(chess_bp)
    db.init_app(app)
    with app.app_context():
        db.create_all()
"""

from .models import db, ChessMember, MatchResult
from .views import chess_bp

__version__ = '1.0.0'
__all__ = ['db', 'ChessMember', 'MatchResult', 'chess_bp']
