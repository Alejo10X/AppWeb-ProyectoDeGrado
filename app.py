import io
import requests

from functools import wraps

from libs.data import dataAnalysis
from libs.wordfile import createReport
from libs.appforms import SignupForm, LoginForm, ChannelForm, ReportForm
from libs.functions import uploadDatetime, generateFileName, dataframeToList
from libs.firebase import signUp, logIn, userDataStorage, getUserData, userFileStorage, userAddFileHistory, getFileURL, getFilesHistory

from flask import Flask, render_template, request, flash, url_for, redirect, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'anotherkey098765'

brand = ' · RS Report'


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged' in session:
            return f(*args, **kwargs)
        else:
            flash('Sin autorización. Por favor inicia sesión', 'danger')
            return redirect(url_for('login'))

    return wrap


# ANCHOR Página de Inicio

@app.route('/')
def home():
    title = 'Inicio' + brand
    return render_template('home.html', title=title)


# ANCHOR User Sign Up / Registro de Usuario

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    title = 'Signup' + brand

    form = SignupForm(request.form)

    if request.method == 'POST' and form.validate():

        userData = {
            'name': form.userName.data.capitalize(),
            'lastname': form.userLastname.data.capitalize(),
            'email': form.emailSign.data,
            'password': form.passwordSign.data
        }

        if signUp(userData['email'], userData['password']) and userDataStorage(userData):

            flash('Ahora te encuentras registrado. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))

        else:
            flash('La cuenta ya existe con el correo que acabas de ingresar. Intenta nuevamente.', 'danger')
            return redirect(url_for('signup'))

    return render_template('signup.html', title=title, form=form)


# ANCHOR User Log In / Inicio de Sesión de Usuario

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login' + brand

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        email = form.emailLog.data
        password = form.passwordLog.data

        if logIn(email, password):

            try:
                session['logged'] = True
                session['user'] = getUserData(email)

                flash('Ahora puedes crear nuevos reportes y descargarlos', 'home')
                return render_template('home.html')

            except:
                flash('Ha ocurrido un error a nivel interno, intenta creando un nuevo usuario', 'danger')
                return redirect(url_for('login'))

        else:
            flash('Error iniciando sesión, el correo o la contraseña no coinciden', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', title=title, form=form)


# ANCHOR User Log Out / Cierre de Sesión de Usuario

@app.route('/logout')
def logout():
    session.clear()
    flash('Has Cerrado la Sesión', 'warning')
    return redirect(url_for('home'))


# ANCHOR Carga de Archivos

@app.route('/upload', methods=['GET', 'POST'])
@is_logged_in
def upload():
    title = 'Seleccionar BD' + brand

    form = ChannelForm(request.form)

    # TODO Verificar que no hayan archivos repetidos, de lo contrario cambiar datos o sobreescribir.

    if request.method == 'POST' and form.validate():

        channel = str(form.channel.data)
        session['channel'] = channel

        api_url = 'https://api.thingspeak.com/channels/{}'.format(channel)
        api_resp = requests.get(api_url + '.json')

        if api_resp.ok:

            session['chInfo'] = api_resp.json()

            filename = generateFileName(0, session['chInfo'])
            file_resp = requests.get(api_url + '/feeds.csv')

            if file_resp.ok:

                f = io.StringIO(file_resp.content.decode('utf-8'))

                userFileStorage(0, session['user']['key'], filename, f)

                session['URL_A'] = getFileURL(0, session['user']['key'], filename)

                session['filedata'] = {
                    'filename': filename,
                    'date': uploadDatetime(),
                    'url': session['URL_A']
                }

                if userAddFileHistory(0, session['user']['key'], session['filedata']):
                    return redirect(url_for('generator'))

                else:
                    flash('Ha ocurrido un error mientras se cargaba el archivo en la base de datos. Intenta de nuevo',
                          'danger')
                    return redirect(url_for('upload'))

            else:
                flash(
                    'El número del Channel ID que escribiste no existe o es incorrecto. Prueba escribiendo otro número.',
                    'danger')
                return redirect(url_for('upload'))

        else:
            flash('El número del Channel ID que escribiste no existe o es incorrecto. Prueba escribiendo otro número.',
                  'danger')
            return redirect(url_for('upload'))

    return render_template('upload.html', title=title, form=form)


# ANCHOR Generador de Reportes - Análisis de Calidad

@app.route('/generator', methods=['GET', 'POST'])
@is_logged_in
def generator():
    title = 'Creación del Reporte' + brand

    form = ReportForm(request.form)

    if request.method == 'POST' and form.validate():

        report_data = {
            'title': form.title.data,
            'author': form.author.data,
            'sendTo': form.sendTo.data,
            'reason': form.reason.data,
            'sourceType': form.sourceType.data,
            'sourceName': form.sourceName.data,
            'zoneName': form.zoneName.data,
            'descrip': form.descript.data
        }

        file_resp = requests.get(session['URL_A'])

        if file_resp.ok:

            analysis = dataAnalysis(io.StringIO(file_resp.content.decode('utf-8')))
            report = createReport(report_data, analysis)

            filename = generateFileName(1, session['chInfo'])

            if userFileStorage(1, session['user']['key'], filename, report):

                session['URL_B'] = getFileURL(1, session['user']['key'], filename)

                session['filedata'] = {
                    'filename': filename,
                    'date': uploadDatetime(),
                    'url': session['URL_B']
                }

                if userAddFileHistory(1, session['user']['key'], session['filedata']):

                    session['dataReview'] = {
                        'Dat': analysis['A'],
                        'Rev': analysis['B'],
                        'Res': dataframeToList(analysis['F']['% Cumplimiento Total']),
                        'Loc': report_data['zoneName'],
                        'pH': dataframeToList(analysis['C']['pH']),
                        'K': dataframeToList(analysis['C']['K']),
                        'OD': dataframeToList(analysis['C']['OD']),
                        'T': dataframeToList(analysis['C']['T'])
                    }

                    return redirect(url_for('review'))

                else:
                    flash('Ha ocurrido un error mientras se cargaba el archivo en la base de datos. Intenta de nuevo',
                          'danger')
                    return redirect(url_for('generator'))

        return redirect(url_for('review'))

    return render_template('generator.html', title=title, form=form)


@app.route('/review')
@is_logged_in
def review():
    title = 'Resumen del Análisis' + brand

    return render_template('review.html', title=title)


@app.route('/map')
@is_logged_in
def map():
    return render_template('map.html')


@app.route('/dashboard')
@is_logged_in
def dashboard():
    title = 'Dashboard' + brand

    up_files = getFilesHistory(0, session['user']['key'])
    gen_files = getFilesHistory(1, session['user']['key'])

    return render_template('dashboard.html', title=title, up_files=up_files, gen_files=gen_files)


@app.route('/about')
def about():
    title = 'Nosotros' + brand
    return render_template('about.html', title=title)


@app.route('/docs')
def docs():
    title = 'Documentación' + brand
    return render_template('docs.html', title=title)


if __name__ == "__main__":
    app.run(debug=False)
