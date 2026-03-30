"""
Chess Club Models
Flask-SQLAlchemy models for member profiles and match results with ranking calculations
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

db = SQLAlchemy()


class ChessMember(db.Model):
    """
    Represents a chess club member
    """
    __tablename__ = 'chess_member'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    current_rank = db.Column(db.Integer, default=1, nullable=False)
    games_played = db.Column(db.Integer, default=0, nullable=False)
    profile_picture = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    matches_as_player1 = db.relationship('MatchResult', foreign_keys='MatchResult.player1_id', backref='player1', cascade='all, delete-orphan')
    matches_as_player2 = db.relationship('MatchResult', foreign_keys='MatchResult.player2_id', backref='player2', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<ChessMember {self.name} {self.surname} (Rank: {self.current_rank})>"

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"

    @property
    def age(self):
        today = date.today()
        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )

    def to_dict(self, include_email=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'full_name': self.full_name,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'age': self.age,
            'current_rank': self.current_rank,
            'games_played': self.games_played,
            'profile_picture': self.profile_picture,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_email:
            data['email'] = self.email
        return data

    def to_dict_public(self):
        """Convert to public profile dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'full_name': self.full_name,
            'age': self.age,
            'current_rank': self.current_rank,
            'games_played': self.games_played,
            'profile_picture': self.profile_picture,
            'bio': self.bio,
        }

    def to_dict_leaderboard(self):
        """Convert to leaderboard dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'current_rank': self.current_rank,
            'games_played': self.games_played,
            'profile_picture': self.profile_picture,
        }


class MatchResult(db.Model):
    """
    Records match results between two players and handles ranking updates
    """
    __tablename__ = 'match_result'

    RESULT_CHOICES = ['player1_win', 'player2_win', 'draw']

    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('chess_member.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('chess_member.id'), nullable=False)
    result = db.Column(db.String(20), nullable=False)  # 'player1_win', 'player2_win', 'draw'
    match_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, default='')

    # Store old ranks for reference
    player1_old_rank = db.Column(db.Integer, nullable=False)
    player2_old_rank = db.Column(db.Integer, nullable=False)
    player1_new_rank = db.Column(db.Integer, nullable=False)
    player2_new_rank = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<MatchResult {self.player1.full_name} vs {self.player2.full_name} - {self.result}>"

    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'player1': self.player1.to_dict_public(),
            'player2': self.player2.to_dict_public(),
            'player1_name': self.player1.full_name,
            'player2_name': self.player2.full_name,
            'result': self.result,
            'match_date': self.match_date.isoformat() if self.match_date else None,
            'notes': self.notes,
            'player1_old_rank': self.player1_old_rank,
            'player2_old_rank': self.player2_old_rank,
            'player1_new_rank': self.player1_new_rank,
            'player2_new_rank': self.player2_new_rank,
            'rank_changes': self.get_rank_changes(),
        }

    def get_rank_changes(self):
        """Get rank changes for both players"""
        return {
            'player1': {
                'old_rank': self.player1_old_rank,
                'new_rank': self.player1_new_rank,
                'change': self.player1_old_rank - self.player1_new_rank
            },
            'player2': {
                'old_rank': self.player2_old_rank,
                'new_rank': self.player2_new_rank,
                'change': self.player2_old_rank - self.player2_new_rank
            }
        }

    def calculate_rank_changes(self):
        """
        Calculate rank changes based on chess club rules:
        1. If higher-ranked player wins: no change
        2. If draw: lower-ranked player gains 1 position (unless adjacent)
        3. If lower-ranked player wins: higher moves down 1, lower moves up by (difference/2)
        """
        p1_rank = self.player1.current_rank
        p2_rank = self.player2.current_rank

        # Determine higher and lower ranked players
        if p1_rank < p2_rank:
            higher_ranked = self.player1
            lower_ranked = self.player2
            p1_is_higher = True
        else:
            higher_ranked = self.player2
            lower_ranked = self.player1
            p1_is_higher = False

        rank_difference = abs(p1_rank - p2_rank)

        if self.result == 'draw':
            # Draw scenario: lower-ranked player gains position (unless adjacent)
            if rank_difference > 1:
                # Lower-ranked player moves up one position
                new_lower_rank = lower_ranked.current_rank - 1
                if p1_is_higher:
                    self.player1_new_rank = p1_rank
                    self.player2_new_rank = new_lower_rank
                else:
                    self.player1_new_rank = new_lower_rank
                    self.player2_new_rank = p2_rank
            else:
                # Adjacent ranks - no change
                self.player1_new_rank = p1_rank
                self.player2_new_rank = p2_rank

        elif (p1_is_higher and self.result == 'player1_win') or \
             (not p1_is_higher and self.result == 'player2_win'):
            # Higher-ranked player wins: no change
            self.player1_new_rank = p1_rank
            self.player2_new_rank = p2_rank

        else:
            # Lower-ranked player wins against higher-ranked player
            # Higher-ranked player moves down 1, lower moves up by (difference/2)
            higher_new_rank = higher_ranked.current_rank + 1
            rank_gain = rank_difference // 2
            lower_new_rank = lower_ranked.current_rank - rank_gain

            if p1_is_higher:
                self.player1_new_rank = higher_new_rank
                self.player2_new_rank = lower_new_rank
            else:
                self.player1_new_rank = lower_new_rank
                self.player2_new_rank = higher_new_rank

    def get_rank_changes(self):
        """Return a dictionary with rank changes for display"""
        return {
            'player1': {
                'name': self.player1.full_name,
                'old_rank': self.player1_old_rank,
                'new_rank': self.player1_new_rank,
                'change': self.player1_old_rank - self.player1_new_rank
            },
            'player2': {
                'name': self.player2.full_name,
                'old_rank': self.player2_old_rank,
                'new_rank': self.player2_new_rank,
                'change': self.player2_old_rank - self.player2_new_rank
            }
        }
