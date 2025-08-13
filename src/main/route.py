from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from database.model import db, User


main_bp = Blueprint('main', __name__, template_folder='templates')


@main_bp.route('/')
def index():
    return render_template('main/index.html', tasks=(current_user.is_authenticated and current_user.tasks))


@main_bp.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        password = request.form['password']
        user = db.session.get(User, current_user.id)

        if check_password_hash(user.password, password):
            for task in user.tasks:
                db.session.delete(task)
            logout_user()
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        flash('Incorrect Password', category='error')
    return render_template('main/delete_account.html')