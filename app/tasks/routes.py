from flask import redirect, url_for, request, Blueprint, abort, flash
from flask_login import login_required, current_user
from app.database import get_task_by_id, add_new_task, delete_task_from_db, toggle_task_status_in_db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/task/create', methods=['POST'])
@login_required
def create_task():
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority = request.form.get('priority', '').strip()
    if not title:
        flash('Назва завдання не може бути порожньою', 'danger')
        return redirect(url_for('auth.index'))
    if priority not in ['Low', 'Medium', 'High']:
        priority = 'Medium'
    add_new_task(title, description, priority, current_user.id)
    return redirect(url_for('auth.index'))

@tasks_bp.route('/task/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        abort(404)
    if task.user_id != current_user.id:
        abort(403)
    toggle_task_status_in_db(task)
    return redirect(url_for('auth.index'))

@tasks_bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = get_task_by_id(task_id)
    if not task:
        abort(404)
    if task.user_id != current_user.id:
        abort(403)
    delete_task_from_db(task)
    return redirect(url_for('auth.index'))
