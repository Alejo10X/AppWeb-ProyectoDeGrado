from wtforms import Form, StringField, PasswordField, ValidationError, TextAreaField, SelectField, IntegerField, validators


def check_email_st(form, field):
    if '@' not in field.data:
        raise ValidationError('El correo debe poseer una arroba (@)')


def check_email_dot(form, field):
    if '.' not in field.data:
        raise ValidationError('El correo debe poseer una extensión de dominio como (.com .co .net) etc.')


def check_empty_text_length(form, field):
    if field.data != '':
        e = ''
        if field.name == 'sendTo':
            e = 'El nombre del destinatario'
        elif field.name == 'descript':
            e = 'La descripción del lugar'

        if len(field.data) <= 4:
            raise ValidationError('{} debe poseer al menos 4 caracteres de longitud'.format(e))


def check_choice(form, field):
    if field.data == '':
        raise ValidationError('Seleccione una opción válida')


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
        check_email_st,
        check_email_dot
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
        check_email_st,
        check_email_dot
    ])

    passwordLog = PasswordField('', [
        validators.Length(min=6, message='La contraseña debe poseer al menos 6 caracteres de longitud'),
        validators.DataRequired('Este campo es requerido')
    ])


class ChannelForm(Form):
    channel = IntegerField('', [
        validators.NumberRange(min=0, max=9999999, message='El número de ID de la base de datos debe poseer entre 5 y 8 caracteres'),
        validators.DataRequired('Este campo es requerido')
    ])


class ReportForm(Form):
    title = StringField('', [
        validators.Length(min=4, message='El título debe poseer al menos 4 caracteres de longitud'),
        validators.DataRequired('Este campo es requerido')
    ])

    author = StringField('', [
        validators.Length(min=3, message='El nombre del autor(es) debe poseer al menos 3 caracteres de longitud'),
        validators.DataRequired('Este campo es requerido')
    ])

    sendTo = StringField('', [
        check_empty_text_length
    ])

    reason = TextAreaField('', [
        validators.DataRequired('Este campo es requerido'),
        validators.Length(min=4, message='La razón debe poseer al menos 4 caracteres de longitud')
    ])

    sourceType = SelectField('', [
        validators.DataRequired('Este campo es requerido'),
        check_choice
    ], choices=[
        ('', 'Selecciona una Opción'),
        ('Arrollo', 'Arrollo'), ('Canal', 'Canal'), ('Charco', 'Charco'), ('Ciénaga', 'Ciénaga'), ('Embalse', 'Embalse'),
        ('Estanque', 'Estanque'), ('Estero', 'Estero'), ('Humedal', 'Humedal'), ('Lago', 'Lago'), ('Laguna', 'Laguna'),
        ('Marisma', 'Marisma'), ('Pantano', 'Pantano'), ('Quebrada', 'Quebrada'), ('Riachuelo', 'Riachuelo'), ('Río', 'Río')
    ])

    sourceName = StringField('', [
        validators.Length(min=3, message='El nombre de la fuente debe poseer al menos 3 caracteres de longitud'),
        validators.DataRequired('Este campo es requerido')
    ])

    zoneName = StringField('', [
        validators.Length(min=4, message='El nombre/ubicación de la zona debe poseer al menos 4 caracteres de longitud'),
        validators.DataRequired('Este campo es requerido')
    ])

    descript = TextAreaField('', [
        check_empty_text_length
    ])
