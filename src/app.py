from flask import Flask
from main.route import main_bp
from auth.route import auth_bp
from tasks.route import task_bp
import config


app = Flask(__name__)
config.config_app(app)
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)


if __name__ == '__main__':
    app.run()
