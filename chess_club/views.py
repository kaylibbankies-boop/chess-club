"""
Chess Club Views (Routes)
Flask routes for member management, leaderboard, and match results
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from .models import db, ChessMember, MatchResult
from datetime import datetime

chess_bp = Blueprint('chess', __name__, url_prefix='/api/chess')


# ===================== Member Routes =====================

@chess_bp.route('/members', methods=['GET'])
def get_members():
    """Get all members sorted by rank"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = ChessMember.query.order_by(ChessMember.current_rank)
        members = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': [m.to_dict() for m in members.items],
            'total': members.total,
            'pages': members.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@chess_bp.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Get a specific member's details"""
    try:
        member = ChessMember.query.get_or_404(member_id)
        return jsonify({'success': True, 'data': member.to_dict(include_email=True)}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@chess_bp.route('/members', methods=['POST'])
def create_member():
    """Create a new chess club member"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'surname', 'email', 'birthday']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(required_fields)}'
            }), 400
        
        # Check if email already exists
        if ChessMember.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 400
        
        # Get the next rank (last rank + 1)
        max_rank_member = ChessMember.query.order_by(ChessMember.current_rank.desc()).first()
        next_rank = (max_rank_member.current_rank + 1) if max_rank_member else 1
        
        member = ChessMember(
            name=data.get('name'),
            surname=data.get('surname'),
            email=data.get('email'),
            birthday=datetime.fromisoformat(data.get('birthday')).date(),
            current_rank=next_rank,
            bio=data.get('bio', ''),
            profile_picture=data.get('profile_picture')
        )
        
        db.session.add(member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Member created successfully',
            'data': member.to_dict(include_email=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@chess_bp.route('/members/<int:member_id>', methods=['PATCH', 'PUT'])
def update_member(member_id):
    """Update member profile"""
    try:
        member = ChessMember.query.get_or_404(member_id)
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data:
            member.name = data['name']
        if 'surname' in data:
            member.surname = data['surname']
        if 'bio' in data:
            member.bio = data['bio']
        if 'profile_picture' in data:
            member.profile_picture = data['profile_picture']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'data': member.to_dict(include_email=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@chess_bp.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete a member"""
    try:
        member = ChessMember.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Member deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@chess_bp.route('/members/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard sorted by ranking"""
    try:
        members = ChessMember.query.order_by(ChessMember.current_rank).all()
        return jsonify({
            'success': True,
            'data': [m.to_dict_leaderboard() for m in members]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@chess_bp.route('/members/<int:member_id>/public-profile', methods=['GET'])
def get_public_profile(member_id):
    """Get public profile of a member"""
    try:
        member = ChessMember.query.get_or_404(member_id)
        return jsonify({
            'success': True,
            'data': member.to_dict_public()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@chess_bp.route('/members/search', methods=['GET'])
def search_members():
    """Search members by name or email"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Please provide a search query'
            }), 400
        
        members = ChessMember.query.filter(
            or_(
                ChessMember.name.ilike(f'%{query}%'),
                ChessMember.surname.ilike(f'%{query}%'),
                ChessMember.email.ilike(f'%{query}%')
            )
        ).order_by(ChessMember.current_rank).all()
        
        return jsonify({
            'success': True,
            'data': [m.to_dict_public() for m in members],
            'count': len(members)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ===================== Match Routes =====================

@chess_bp.route('/matches', methods=['GET'])
def get_matches():
    """Get all matches"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = MatchResult.query.order_by(MatchResult.match_date.desc())
        matches = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': [m.to_dict() for m in matches.items],
            'total': matches.total,
            'pages': matches.pages,
            'current_page': page
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@chess_bp.route('/matches/recent', methods=['GET'])
def get_recent_matches():
    """Get the last 10 matches"""
    try:
        matches = MatchResult.query.order_by(MatchResult.match_date.desc()).limit(10).all()
        return jsonify({
            'success': True,
            'data': [m.to_dict() for m in matches]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@chess_bp.route('/matches/record', methods=['POST'])
def record_match():
    """Record a new match and update rankings"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['player1_id', 'player2_id', 'result']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(required_fields)}'
            }), 400
        
        player1_id = data.get('player1_id')
        player2_id = data.get('player2_id')
        result = data.get('result')
        
        # Validate players are different
        if player1_id == player2_id:
            return jsonify({
                'success': False,
                'error': 'A player cannot play against themselves'
            }), 400
        
        # Validate result
        if result not in MatchResult.RESULT_CHOICES:
            return jsonify({
                'success': False,
                'error': f'Invalid result. Must be one of: {", ".join(MatchResult.RESULT_CHOICES)}'
            }), 400
        
        # Get players
        player1 = ChessMember.query.get(player1_id)
        player2 = ChessMember.query.get(player2_id)
        
        if not player1 or not player2:
            return jsonify({
                'success': False,
                'error': 'One or both players not found'
            }), 404
        
        # Create match and calculate rankings
        match = MatchResult(
            player1_id=player1_id,
            player2_id=player2_id,
            result=result,
            notes=data.get('notes', ''),
            player1_old_rank=player1.current_rank,
            player2_old_rank=player2.current_rank
        )
        
        # Calculate new ranks
        match.calculate_rank_changes()
        
        # Update player ranks
        player1.current_rank = match.player1_new_rank
        player2.current_rank = match.player2_new_rank
        player1.games_played += 1
        player2.games_played += 1
        
        # Save everything
        db.session.add(match)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Match recorded successfully',
            'data': match.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@chess_bp.route('/matches/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Get a specific match"""
    try:
        match = MatchResult.query.get_or_404(match_id)
        return jsonify({
            'success': True,
            'data': match.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404
