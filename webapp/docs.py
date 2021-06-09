from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)

bp = Blueprint('/docs', __name__)


@bp.route('/docs')
def docs():
    return render_template('web/docs/docs.html')
