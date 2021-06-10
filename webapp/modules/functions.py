from datetime import datetime
from werkzeug.utils import secure_filename


def upload_datetime():
    datetimes = datetime.now().strftime('%x %I:%M:%S %p')

    return datetimes


def gen_file_name(sel, data):

    txtname = data['name'].split(' - ')[1]

    if 'Default' in txtname:
        txtname = txtname.split(' ')[0]

    if sel == 0:
        filename = 'DataFile_{}.csv'.format(txtname)
    elif sel == 1:
        filename = 'ReportFile_{}.docx'.format(txtname)
    else:
        raise print('Debe seleccionar únicamente los valores 1 o 2')

    return secure_filename(filename)
