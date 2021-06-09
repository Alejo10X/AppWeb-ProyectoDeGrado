from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def home():
    title = 'Inicio · RS Report'
    return render_template('home.html', title=title)
