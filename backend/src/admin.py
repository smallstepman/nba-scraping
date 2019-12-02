from flask_admin.contrib.sqla import ModelView

from .extensions import db, admin
from .models.game import Game, QuarterScore, Team

class MyView(ModelView):
    column_display_pk = True 
    column_display_fk = True 

admin.add_view(MyView(Game, db.session))
admin.add_view(MyView(QuarterScore, db.session))
admin.add_view(MyView(Team, db.session))