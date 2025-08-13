from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from database.model import db, Task


task_bp = Blueprint('task', __name__, template_folder='templates')


@task_bp.route('/tasks')
@login_required
def tasks():
    length = len(list(filter(lambda item: not item.completed, current_user.tasks)))
    return render_template('tasks/tasks.html', tasks=current_user.tasks, tasks_incomplet_length=length)


@task_bp.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        task = Task(title=title, description=description, user=current_user)
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('task.tasks'))
    return render_template('tasks/create_task.html')


@task_bp.route('/completed_task', methods=['POST'])
@login_required
def completed_task():
    if request.method == 'POST':
        id = int(request.form['id'])
        task = db.session.get(Task, id)
        task.completed = True
        db.session.commit()
    return redirect(url_for('task.tasks'))


@task_bp.route('/deleted_task', methods=['POST'])
@login_required
def deleted_task():
    if request.method == 'POST':
        id = int(request.form['id'])
        task = db.session.get(Task, id)
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('task.tasks'))


@task_bp.route('/reopen_task', methods=['POST'])
@login_required
def reopen_task():
    if request.method == 'POST':
        id = int(request.form['id'])
        task = db.session.get(Task, id)
        task.completed = False
        db.session.commit()
    return redirect(url_for('task.tasks'))