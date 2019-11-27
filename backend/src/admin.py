from flask_admin.contrib.sqla import ModelView

from .extensions import db, admin
from .models.game import Game

admin.add_view(ModelView(Game, db.session))