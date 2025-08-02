from flask import render_template
from flask_login import LoginManager
from database import init_database
from database.model import User


def config_app(app):
    app.secret_key = 'fgvhbjiuy76t5rtfghjkiouy76t5r4eertyu8y7tf'

    # Configure LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    init_database(app, __file__)


    @login_manager.user_loader
    def load_user(user_id: str) -> User:
        return User.get(user_id)


    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404
    

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html'), 500