from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.database import create_user, get_user_by_username, get_user_by_email, get_tasks_for_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    user_tasks = []
    if current_user.is_authenticated:
        user_tasks = get_tasks_for_user(current_user.id)
    return render_template('index.html', tasks=user_tasks)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        if not username or not email or not password:
            flash('Всі поля обов’язкові для заповнення', 'danger')
            return redirect(url_for('auth.register'))
        if get_user_by_username(username) or get_user_by_email(email):
            flash('Користувач з таким логіном або email вже існує', 'danger')
            return redirect(url_for('auth.register'))
        create_user(username, email, password)
        flash('Реєстрація успішна! Тепер ви можете увійти.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Всі поля обов’язкові для заповнення', 'danger')
            return redirect(url_for('auth.login'))
        user = get_user_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('auth.index'))
        flash('Неправильний логін або пароль', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.index'))
