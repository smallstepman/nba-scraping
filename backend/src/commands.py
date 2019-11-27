import click 
from flask.cli import with_appcontext 

from .extensions import db
from .models.game import Game

@click.command(name='create_database')
@with_appcontext
def create_db_command():
    db.create_all() 

@click.command(name='create_game')
@with_appcontext
def insert_records_command():
    g = Game(winning_team='team 1',
         losing_team='team 2',
         score='0:0')
    db.session.add(g)
    db.session.commit()