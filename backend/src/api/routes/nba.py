from flask import jsonify

from ...models.game import Game, QuarterScore, QuarterScoreSchema, GameSchema

def get_games_by_date(date):
    games = Game.query.filter(
        Game.date == date
    )
    game_schema = GameSchema(many=True)
    # print(games)
    return jsonify(game_schema.dump(games))


def get_game_details(game_id):
    return game_id