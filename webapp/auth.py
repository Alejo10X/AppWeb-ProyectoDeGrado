from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)

from webapp.modules.forms import SignupForm, LoginForm
from webapp.modules.database import sign_up, log_in, get_user_data

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    title = 'Signup · RS Report'

    form = SignupForm(request.form)

    if request.method == 'POST' and form.validate():

        userData = {
            'name': form.userName.data.capitalize(),
            'lastname': form.userLastname.data.capitalize(),
            'email': form.emailSign.data,
            'password': form.passwordSign.data
        }

        if sign_up(userData['email'], userData['password']):

            flash('Ahora te encuentras registrado. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))

        else:
            flash('La cuenta ya existe con el correo que acabas de ingresar. Intenta nuevamente.', 'danger')
            return redirect(url_for('auth.signup'))

    return render_template('web/auth/signup.html', title=title, form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    title = 'Login · RS Report'

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():

        email = form.emailLog.data
        password = form.passwordLog.data

        if log_in(email, password):

            try:
                session['logged'] = True
                session['user'] = get_user_data(email)

                flash('Ahora puedes crear nuevos reportes y descargarlos', 'home')
                return redirect(url_for('home.home'))

            except:
                flash('Ha ocurrido un error a nivel interno, intenta creando un nuevo usuario', 'danger')
                return redirect(url_for('auth.login'))

        else:
            flash('Error iniciando sesión, el correo o la contraseña no coinciden', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('web/auth/login.html', title=title, form=form)


@bp.route('/logout')
def logout():
    session.clear()
    flash('Has Cerrado la Sesión', 'warning')

    return redirect(url_for('home.home'))
