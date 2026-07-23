from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import create_app
from app.database import db
from app.models import User, Task

app = create_app()


@app.route('/')
def index():
    if current_user.is_authenticated:
        user_tasks = Task.query.filter_by(user_id=current_user.id).all()
        tasks_html = ""
        for task in user_tasks:
            status = "Виконано" if task.is_completed else "В роботі"
            tasks_html += f'''
                <li>
                    <b>{task.title}</b> ({task.priority}) - {status}<br>
                    {task.description}<br>
                    <a href="/task/{task.id}/toggle">[Змінити статус]</a>
                    <a href="/task/{task.id}/delete" style="color:red;">[Видалити]</a>
                </li><br>
            '''

        dog_avatar_url = url_for('static', filename='Buch.jpg')

        return f'''
            <div style="display: flex; align-items: center; gap: 15px;">
                <img src="{dog_avatar_url}" alt="Dog Avatar" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover;">
                <h1>Панель завдань користувача {current_user.username}</h1>
            </div>
            <br>
            <a href="/logout">Вийти з аккаунта</a>
            <hr>
            <h3>Створити нове завдання</h3>
            <form method="post" action="/task/create">
                Назва: <input type="text" name="title" required><br>
                Опис: <textarea name="description"></textarea><br>
                Пріоритет: 
                <select name="priority">
                    <option value="Low">Low</option>
                    <option value="Medium" selected>Medium</option>
                    <option value="High">High</option>
                </select><br>
                <input type="submit" value="Додати завдання">
            </form>
            <hr>
            <h3>Список ваших завдань</h3>
            <ul>{tasks_html}</ul>
        '''
    return "<h1>TaskFlow</h1><a href='/login'>Увійти</a> або <a href='/register'>Зареєструватися</a>"


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return "Користувач вже існує", 400
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return '''
        <h2>Реєстрація</h2>
        <form method="post">
            Username: <input type="text" name="username" required><br>
            Email: <input type="email" name="email" required><br>
            Password: <input type="password" name="password" required><br>
            <input type="submit" value="Register">
        </form>
    '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        return "Неправильні дані", 401
    return '''
        <h2>Вхід у систему</h2>
        <form method="post">
            Username: <input type="text" name="username" required><br>
            Password: <input type="password" name="password" required><br>
            <input type="submit" value="Login">
        </form>
    '''


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/task/create', methods=['POST'])
@login_required
def create_task():
    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    new_task = Task(title=title, description=description, priority=priority, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/task/<int:task_id>/toggle')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.is_completed = not task.is_completed
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/task/<int:task_id>/delete')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
