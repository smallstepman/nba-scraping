from marshmallow import fields

from ..extensions import db, marshall



class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(35))
    logo_url = db.Column(db.String(254))

    def __repr__(self):
        return self.name


class Game(db.Model):
    espn_game_id = db.Column(db.Integer, primary_key=True, nullable=False)
    date = db.Column(db.DateTime)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team = db.relationship("Team", foreign_keys=[home_team_id])
    home_team = db.relationship("Team", foreign_keys=[away_team_id])
    quarter_scores = db.relationship('QuarterScore', backref='game', lazy=True)

    def __repr__(self):
        return f"{self.home_team} - {self.away_team}" 

    def away_team_score(self):
        return sum(qs.away_team_score for qs in self.quarter_scores)

    def home_team_score(self):
        return sum(qs.home_team_score for qs in self.quarter_scores)

    def winner(self):
        return ("home team" if 
        self.home_team_score() > self.away_team_score()
        else "away team")


class QuarterScore(db.Model):
    """
        I'm fullt aware that splitting this into separate table 
        is a bad idea :), mostly because putting it into game table 
        would incrise readability 
        A1   A2   A3   A4    H1   H2   H3   H4
        12 | 12 | 45 | 45    10 | 12 | 45 | 45
    """
    id = db.Column(db.Integer, primary_key=True)    
    espn_game_id = db.Column(db.Integer, db.ForeignKey('game.espn_game_id'))
    quarter_count = db.Column(db.Integer)
    away_team_score = db.Column(db.Integer)
    home_team_score = db.Column(db.Integer)
     

    def __repr__(self):
        return f"{self.quarter_count}: {self.home_team_score} - {self.away_team_score}"



class QuarterScoreSchema(marshall.Schema):
    class Meta:
        model = QuarterScore
        fields = ('game_id', 'quarter_count', 
                  'away_team_score', 'home_team_score')



class GameSchema(marshall.Schema):
    class Meta:
        model = Game
        fields = ('id', 'date', 'home_team', 'away_team', 'quarter_scores','home_score','away_score')
        
    quarter_scores = marshall.Nested(QuarterScoreSchema, 
                                     many=True,
                                     only=['quarter_count', 
                                           'away_team_score', 
                                           'home_team_score'])
    home_team = 
    away_team = 
    away_score = fields.Method("away_team_score")
    home_score = fields.Method("home_team_score")

    def home_team_score(self, obj):
        return obj.home_team_score()

    def away_team_score(self, obj):
        return obj.away_team_score()
    
