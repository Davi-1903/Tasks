from database.model import db
import os


def init_database(app):
    os.makedirs(app.instance_path, exist_ok=True) # Create database directory case doesn't exist
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{app.instance_path}/data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Create database
    with app.app_context():
        db.create_all()
