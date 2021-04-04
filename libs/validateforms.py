from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import Form, StringField, PasswordField, ValidationError, validators


def checkEmailArr(form, field):
    if '@' not in field.data:
        raise ValidationError('El correo debe poseer una arroba (@)')

def checkEmailDot(form, field):
    if '.' not in field.data:
        raise ValidationError('El correo debe poseer una extensión de dominio como (.com .co .net) etc.')



class SignupForm(Form):

    userName = StringField('', [
        validators.DataRequired('Este campo es requerido')
    ])

    userLastname = StringField('', [
        validators.DataRequired('Este campo es requerido')
    ])

    emailSign = StringField('', [
        validators.Length(min=6, message='El correo debe poseer al menos 6 caracteres de longitud'),
        validators.DataRequired('Este campo es requerido'),
        checkEmailArr,
        checkEmailDot
    ])

    passwordSign = PasswordField('', [
        validators.Length(min=6, message='La contraseña debe poseer al menos 6 caracteres de longitud'),
        validators.DataRequired('Este campo es requerido'),
        validators.EqualTo('confirm', 'Las contraseñas escritas no coinciden')
    ])

    confirm = PasswordField('')



class LoginForm(Form):
    emailLog = StringField('', [
        validators.Length(min=6, message='El correo debe poseer al menos 6 caracteres de longitud'),
        validators.DataRequired('Este campo es requerido'),
        checkEmailArr,
        checkEmailDot
    ])

    passwordLog = PasswordField('', [
        validators.Length(min=6, message='La contraseña debe poseer al menos 6 caracteres de longitud'),
        validators.DataRequired('Este campo es requerido')
    ])
