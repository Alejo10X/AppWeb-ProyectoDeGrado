import locale
import pandas as pd
from datetime import datetime

from werkzeug.utils import secure_filename

locale.setlocale(locale.LC_TIME, 'es_CO')


def uploadDatetime():
    datetimes = datetime.now().strftime('%x %X')

    return datetimes


def generateFileName(selector, data):

    txtname = data['name'].split(' - ')[1]

    if 'Default' in txtname:
        txtname = txtname.split(' ')[0]

    if selector == 1:
        filename = 'DataFile_{}.csv'.format(txtname)
    else:
        filename = 'ReportFile_{}.docx'.format(txtname)

    return secure_filename(filename)


def dataframeToList(df):
    return df.tolist()
