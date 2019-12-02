import os
from pathlib import Path

import connexion

from .api import get_bundled_specs
from .admin import *
from .models import *
from .extensions import db, admin, cors, marshall
from .commands import create_db_command, insert_records_command

def create_app():

    connexion_app = connexion.FlaskApp(__name__, specification_dir='api/')
    connexion_app.add_api(
        get_bundled_specs(
            Path(connexion_app.specification_dir, 'main.yaml')))
    app = flask_app = connexion_app.app

    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQLALCHEMY_ECHO=True,
        SECRET_KEY=os.environ.get('SECRET_KEY')
    )

    app.cli.add_command(create_db_command)
    app.cli.add_command(insert_records_command)

    db.init_app(app)
    admin.init_app(app)
    marshall.init_app(app)
    cors.init_app(app)

    return app
