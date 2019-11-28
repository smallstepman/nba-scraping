from datetime import date

import click 
from flask.cli import with_appcontext 

from .extensions import db
from .models.game import Game, QuarterScore

@click.command(name='create_database')
@with_appcontext
def create_db_command():
    # db.session.commit()   #<--- solution!
    # db.drop_all()
    db.create_all() 

@click.command(name='create_game')
@with_appcontext
def insert_records_command():
    g = Game(
        id = 123123,
        date = date(2019,10,10),
        away_team='team 1',
        home_team='team 2')
    db.session.add(g)
    db.session.commit()