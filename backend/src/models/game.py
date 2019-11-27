from ..extensions import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    winning_team = db.Column(db.String(30))
    losing_team = db.Column(db.String(30))
    score = db.Column(db.String(30))
    # game_details = db.relationship()