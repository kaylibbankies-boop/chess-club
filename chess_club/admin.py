"""
Chess Club Admin Routes (Optional)
Not automatically included, but you can add admin routes here if needed.

Example Flask admin route for adding members:
"""
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import db, ChessMember, MatchResult
from datetime import datetime

admin_bp = Blueprint('chess_admin', __name__, url_prefix='/admin/chess')

# Example route to manage members (would need admin authentication in production)
@admin_bp.route('/members', methods=['GET'])
def admin_members():
    """Admin page to view and manage members"""
    members = ChessMember.query.order_by(ChessMember.current_rank).all()
    return {'members': [m.to_dict() for m in members]}

# To register in your Flask app:
# from chess_club.admin import admin_bp
# app.register_blueprint(admin_bp)
