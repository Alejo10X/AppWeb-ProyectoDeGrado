import pyrebase
from requests import HTTPError

firebaseConfig = {
    'apiKey': "AIzaSyCePI5JkqUiG0ILwG6A45f_xctb77lznk8",
    'authDomain': "rs-report-generator.firebaseapp.com",
    'databaseURL': "https://rs-report-generator-default-rtdb.firebaseio.com",
    'projectId': "rs-report-generator",
    'storageBucket': "rs-report-generator.appspot.com",
    'messagingSenderId': "335249771303",
    'appId': "1:335249771303:web:49f88f1475be8e5b677702"
}

firebase = pyrebase.initialize_app(firebaseConfig)

sel_list = ('UploadedFiles', 'GeneratedFiles')


def sign_up(email, password):
    """Creación de usuario en Firebase Auth"""
    auth = firebase.auth()

    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user['idToken'])

    except HTTPError as e:
        e = eval(e.__str__().split('] ')[1]).get('error').get('message')
        print(e)
        # TODO: validar el tipo de mensaje y retornarlo para generar una alerta específica
        return False

    return True


def log_in(email, password):
    """Inicio de sesión de usuario en Firebase Auth"""
    auth = firebase.auth()

    try:
        auth.sign_in_with_email_and_password(email, password)

    except HTTPError as e:
        e = eval(e.__str__().split('] ')[1]).get('error').get('message')
        print(e)

        return False

    return True


def user_data_storage(data, user):
    """Crea un nuevo registro en la base de datos, almacenando los datos del nuevo usuario."""
    db = firebase.database()

    try:
        db.child('users').child(user).set(data)
    except HTTPError:
        return False

    return True


def get_user_data(email):
    """ Obtiene los datos del usuario alojados en en la base de datos"""
    db = firebase.database()
    users = db.child('users').order_by_child('email').equal_to(email).get()

    for user in users.each():

        if user.val()['email'] == email:

            data = {
                'key': user.key(),
                'data': user.val()
            }

            return data

        else:
            return None


def files_storage(sel, userkey, filename, f):
    """Almacena los archivos del usuario, o los generados en el sistema dentro de Firebase"""
    storage = firebase.storage()

    try:
        if sel == 0 or sel == 1:
            path = '{}/{}/{}'.format(sel_list[sel], userkey, filename)
            storage.child(path).put(f)
        else:
            raise print('Debe seleccionar únicamente los valores 1 o 2')
    except HTTPError:
        return False

    return True


def get_files_url(sel, userkey, filename):
    """Obtiene la dirección URL de un archivo alojado en la base de datos de Firebase,
    para luego permitir la descarga al usuario"""
    storage = firebase.storage()

    try:
        if sel == 0 or sel == 1:
            path = '{}/{}/{}'.format(sel_list[sel], userkey, filename)
            url = storage.child(path).get_url(None)
        else:
            raise print('El valor de selección debe ser únicamente los valores 1 o 2')
    except HTTPError:
        return None

    return url


def add_files_hist(sel, userkey, filedata):
    """Crea un nuevo registro dentro de la base de datos, almacenando los datos del archivo
    cargado por el usuario o generado por el sistema. Los datos a almacenar son: nombre del archivo,
    fecha/hora de creación y URL de Firebase"""
    db = firebase.database()

    try:
        if sel == 0 or sel == 1:
            db.child('users').child(userkey).child(sel_list[sel]).push(filedata)
        else:
            raise print('El valor de selección debe ser únicamente los valores 1 o 2')
    except HTTPError:
        return False

    return True


def get_files_hist(sel, userkey):
    """Obtiene el historial de registros de los archivos cargados y generados, asociados a la
    cuenta de un usuario específico"""
    db = firebase.database()

    if sel == 0 or sel == 1:
        user_hist = db.child('users').child(userkey).child(sel_list[sel]).get()
    else:
        raise print('El valor de selección debe ser únicamente los valores 1 o 2')

    files_list = []
    if user_hist.val() is not None:
        for data in user_hist.each():
            files_list.append(data.val())

        files_list.reverse()

    return files_list
