from app.auth import auth
from flask_login import current_user, login_user, logout_user
from flask import redirect, url_for, flash, render_template
from app.auth.forms import LoginForm, RegisterForm
from app.models import User
from app import db

@auth.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('auth/index.html', title='Bem-vindo')
    
        
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.user_name.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuário ou senha invalidos')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('auth.index'))
    return render_template('auth/login.html', title= 'Entrar', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, user_name=form.user_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, o usuário foi registrado com sucesso!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Registrar', form=form)


