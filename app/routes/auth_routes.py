from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.usuario import Usuario

bp = Blueprint('auth', __name__)

@bp.route('/auth', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Usuario.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            flash("Sesion iniciada!", "success")
            return redirect(url_for('auth.dashboard'))
        
        flash('Datos incorrectos. Por favor intentalo nuevamente.', 'danger')
    
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard'))
    return render_template("auth/login.html")

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Cerraste sesion exitosamente.', 'info')
    return redirect(url_for('auth.login'))