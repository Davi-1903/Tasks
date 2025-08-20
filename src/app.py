from flask import Flask
from main.routes import main_bp
from auth.routes import auth_bp
from tasks.routes import task_bp
import config


app = Flask(__name__, instance_relative_config=True)
config.config_app(app)
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)


if __name__ == '__main__':
    app.run()
