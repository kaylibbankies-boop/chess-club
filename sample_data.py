"""
Sample Data Script
Populate the database with test data for development
"""
from app import create_app, db
from chess_club.models import ChessMember, MatchResult
from datetime import date, datetime, timedelta

def create_sample_data():
    """Create sample chess members and match results"""
    
    app = create_app('development')
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        print("Database reset and recreated")
        
        # Create sample members
        members = [
            ChessMember(
                name="Alice",
                surname="Johnson",
                email="alice@chess.local",
                birthday=date(1990, 5, 15),
                current_rank=1,
                bio="Chess Master - 20 years experience",
                games_played=0
            ),
            ChessMember(
                name="Bob",
                surname="Smith",
                email="bob@chess.local",
                birthday=date(1992, 8, 22),
                current_rank=2,
                bio="Intermediate player - loves tactics",
                games_played=0
            ),
            ChessMember(
                name="Charlie",
                surname="Brown",
                email="charlie@chess.local",
                birthday=date(1995, 3, 10),
                current_rank=3,
                bio="Rising star - promising young talent",
                games_played=0
            ),
            ChessMember(
                name="Diana",
                surname="Wilson",
                email="diana@chess.local",
                birthday=date(1988, 11, 30),
                current_rank=4,
                bio="Chess coach and analyst",
                games_played=0
            ),
            ChessMember(
                name="Eve",
                surname="Davis",
                email="eve@chess.local",
                birthday=date(1997, 2, 14),
                current_rank=5,
                bio="Beginner - just started playing",
                games_played=0
            ),
        ]
        
        for member in members:
            db.session.add(member)
        
        db.session.commit()
        print(f"✓ Created {len(members)} members")
        
        # Create sample match results
        matches = [
            MatchResult(
                player1_id=1,
                player2_id=2,
                result='player1_win',
                notes='Great endgame by Alice',
                player1_old_rank=1,
                player2_old_rank=2,
                player1_new_rank=1,
                player2_new_rank=2,
                match_date=datetime.now() - timedelta(days=5)
            ),
            MatchResult(
                player1_id=2,
                player2_id=3,
                result='player1_win',
                notes='Solid positional play',
                player1_old_rank=2,
                player2_old_rank=3,
                player1_new_rank=2,
                player2_new_rank=3,
                match_date=datetime.now() - timedelta(days=4)
            ),
            MatchResult(
                player1_id=3,
                player2_id=4,
                result='draw',
                notes='Tense match, both played well',
                player1_old_rank=3,
                player2_old_rank=4,
                player1_new_rank=3,
                player2_new_rank=4,
                match_date=datetime.now() - timedelta(days=3)
            ),
            MatchResult(
                player1_id=5,
                player2_id=4,
                result='player2_win',
                notes='Beginner upset! Eve nearly won',
                player1_old_rank=5,
                player2_old_rank=4,
                player1_new_rank=5,
                player2_new_rank=4,
                match_date=datetime.now() - timedelta(days=2)
            ),
            MatchResult(
                player1_id=1,
                player2_id=3,
                result='player1_win',
                notes='Decisive victory',
                player1_old_rank=1,
                player2_old_rank=3,
                player1_new_rank=1,
                player2_new_rank=3,
                match_date=datetime.now() - timedelta(days=1)
            ),
        ]
        
        for match in matches:
            db.session.add(match)
            # Update player stats
            match.player1.games_played += 1
            match.player2.games_played += 1
        
        db.session.commit()
        print(f"✓ Created {len(matches)} matches")
        
        # Refresh and update games_played
        db.session.refresh(db.session.query(ChessMember).all())
        
        print("\n✓ Sample data created successfully!")
        print("\nMembers:")
        for member in ChessMember.query.order_by(ChessMember.current_rank).all():
            print(f"  {member.current_rank}. {member.full_name} (Rank: {member.current_rank}, Games: {member.games_played})")
        
        print("\nRecent matches:")
        for match in MatchResult.query.order_by(MatchResult.match_date.desc()).limit(5).all():
            print(f"  {match.player1.full_name} vs {match.player2.full_name} - {match.result}")


if __name__ == '__main__':
    create_sample_data()
