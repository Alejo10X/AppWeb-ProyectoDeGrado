import io
import requests
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)

from webapp import is_logged_in

from webapp.modules.wordreport import gen_report
from webapp.modules.analyzer import data_analysis
from webapp.modules.forms import ChannelForm, ReportForm
from webapp.modules.functions import upload_datetime, gen_file_name
from webapp.modules.database import files_storage, get_files_url, add_files_hist, get_files_hist


bp = Blueprint('main', __name__)


@bp.route('/channel', methods=('GET', 'POST'))
def channel():
    title = 'Seleccionar BD · RS Report'

    form = ChannelForm(request.form)

    # TODO Verificar que no hayan archivos repetidos, de lo contrario cambiar datos o sobreescribir.

    if request.method == 'POST' and form.validate():

        user_channel = str(form.channel.data)
        session['channel'] = user_channel

        api_url = 'https://api.thingspeak.com/channels/{}'.format(user_channel)
        api_resp = requests.get(api_url + '.json')

        if api_resp.ok:

            session['chInfo'] = api_resp.json()

            filename = gen_file_name(0, session['chInfo'])
            file_resp = requests.get(api_url + '/feeds.csv')

            if file_resp.ok:

                f = io.StringIO(file_resp.content.decode('utf-8'))

                files_storage(0, session['user']['key'], filename, f)

                session['URL_A'] = get_files_url(0, session['user']['key'], filename)

                session['filedata'] = {
                    'filename': filename,
                    'date': upload_datetime(),
                    'url': session['URL_A']
                }

                if add_files_hist(0, session['user']['key'], session['filedata']):
                    return redirect(url_for('main.report'))

                else:
                    flash('Ha ocurrido un error mientras se cargaba el archivo en la base de datos. Intenta de nuevo',
                          'danger')
                    return redirect(url_for('main.channel'))

            else:
                flash(
                    'El número del Channel ID que escribiste no existe o es incorrecto. Prueba escribiendo otro número.',
                    'danger')
                return redirect(url_for('main.channel'))

        else:
            flash('El número del Channel ID que escribiste no existe o es incorrecto. Prueba escribiendo otro número.',
                  'danger')
            return redirect(url_for('main.channel'))

    return render_template('web/main/channel.html', title=title, form=form)


@bp.route('/report', methods=('GET', 'POST'))
@is_logged_in
def report():
    title = 'Creación del Reporte · RS Report'

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

            analysis = data_analysis(io.StringIO(file_resp.content.decode('utf-8')))
            rep_file = gen_report(report_data, analysis)

            filename = gen_file_name(1, session['chInfo'])

            if files_storage(1, session['user']['key'], filename, rep_file):

                session['URL_B'] = get_files_url(1, session['user']['key'], filename)

                session['filedata'] = {
                    'filename': filename,
                    'date': upload_datetime(),
                    'url': session['URL_B']
                }

                if add_files_hist(1, session['user']['key'], session['filedata']):

                    session['dataReview'] = {
                        'Dat': analysis['A'],
                        'Rev': analysis['B'],
                        'Res': analysis['F']['% Cumplimiento Total'].tolist(),
                        'Loc': report_data['zoneName'],
                        'pH': analysis['C']['pH'].tolist(),
                        'K': analysis['C']['K'].tolist(),
                        'OD': analysis['C']['OD'].tolist(),
                        'T': analysis['C']['T'].tolist()
                    }

                    return redirect(url_for('main.data'))

                else:
                    flash('Ha ocurrido un error mientras se cargaba el archivo en la base de datos. Intenta de nuevo',
                          'danger')
                    return redirect(url_for('main.report'))

        return redirect(url_for('main.data'))

    return render_template('web/main/report.html', title=title, form=form)


@bp.route('/data')
@is_logged_in
def data():
    title = 'Resumen del Análisis · RS Report'

    return render_template('web/main/data.html', title=title)


@bp.route('/map')
@is_logged_in
def render_map():
    return render_template('web/main/map.html')


@bp.route('/dashboard')
@is_logged_in
def dashboard():
    title = 'Dashboard · RS Report'

    up_files = get_files_hist(0, session['user']['key'])
    gen_files = get_files_hist(1, session['user']['key'])

    return render_template('web/main/fileshist.html', title=title, up_files=up_files, gen_files=gen_files)

