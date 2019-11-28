from flask_admin.contrib.sqla import ModelView

from .extensions import db, admin
from .models.game import Game, QuarterScore

admin.add_view(ModelView(Game, db.session))
admin.add_view(ModelView(QuarterScore, db.session))