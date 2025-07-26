from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.model import db, User, Task
import os


app = Flask(__name__)
app.secret_key = 'fgvhbjiuy76t5rtfghjkiouy76t5r4eertyu8y7tf'

# Configure LoginManager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Configure database
PATH = os.path.dirname(__file__)
os.makedirs(f'{PATH}/database', exist_ok=True) # Create database directory case doesn't exist
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}/database/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id: str) -> User:
    return User.get(user_id)


# ================================================ ROTAS ================================================
@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', tasks=current_user.tasks)
    return render_template('index.html', tasks=None)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('This email doesn\'t exist', category='error')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if not user:
            new_user = User(name=name, email=email, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('index'))
        else:
            flash('Already a user with this email', category='error')

    return render_template('register.html')


@app.route('/tasks')
@login_required
def tasks():
    length = len(list(filter(lambda item: not item.completed, current_user.tasks)))
    return render_template('tasks.html', tasks=current_user.tasks, tasks_incomplet_length=length)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        task = Task(title=title, description=description, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('tasks'))
    return render_template('create_task.html')


@app.route('/completed_task', methods=['POST'])
@login_required
def completed_task():
    if request.method == 'POST':
        id = int(request.form['id'])
        task = Task.query.get(id)
        task.completed = True
        db.session.commit()
    return redirect(url_for('tasks'))


@app.route('/deleted_task', methods=['POST'])
@login_required
def deleted_task():
    if request.method == 'POST':
        id = request.form['id']
        task = Task.query.get(int(id))
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('tasks'))


@app.route('/reopen_task', methods=['POST'])
@login_required
def reopen_task():
    if request.method == 'POST':
        id = int(request.form['id'])
        task = Task.query.get(id)
        task.completed = False
        db.session.commit()
    return redirect(url_for('tasks'))