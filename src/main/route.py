from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import logout_user, login_required, current_user
from database.model import db, User


main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route('/')
def index():
    return render_template('main/index.html', tasks=(current_user.is_authenticated and current_user.tasks))


@main_bp.route('/delete_account/<int:user_id>', methods=['POST'])
@login_required
def delete_account(user_id):
    if request.method == 'POST':
        user = db.session.get(User, user_id)
        for task in user.tasks:
            db.session.delete(task)
        logout_user()
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('main.index'))