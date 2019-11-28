from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
admin = Admin(name="Admin")
marshall = Marshmallow()
migrate = Migrate()