from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from flask_babel import _, lazy_gettext as _l

from app.models import User

DATA_REQUIRED_LABEL = 'Esse campo é obrigatório!'
MAX_LENGTH_LABEL = 'Esse campo pode conter no máximo %i caracteres!'
EQUAL_FIELD_LABEL = 'O valor desse campo deve ser igual ao do campo %s!'
EMAIL_FIELD_LABEL = 'O valor desse campo deve ser um endereço de email válido!'


class LoginForm(FlaskForm):
    username = StringField(_l('Usuário'), validators=[DataRequired(DATA_REQUIRED_LABEL)])
    password = PasswordField(_l('Senha'), validators=[DataRequired(DATA_REQUIRED_LABEL)])
    remember_me = BooleanField(_l('Lembrar'))
    submit = SubmitField(_l('Logar'))


class RegistrationForm(FlaskForm):
    username = StringField(_l('Usuário'), validators=[DataRequired(DATA_REQUIRED_LABEL),
                                                      Length(max=64, message=MAX_LENGTH_LABEL % 64)])
    email = StringField(_l('E-mail'),
                        validators=[DataRequired(DATA_REQUIRED_LABEL), Email(EMAIL_FIELD_LABEL), Length(max=120)])
    password = PasswordField(_l('Senha'), validators=[DataRequired(DATA_REQUIRED_LABEL)])
    password2 = PasswordField(_l('Repita a senha'), validators=[EqualTo('password', EQUAL_FIELD_LABEL % 'senha'),
                                                                DataRequired(DATA_REQUIRED_LABEL)])
    submit = SubmitField(_l('Registrar'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_('Por favor escolha outro nome de usuário.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(_('Por favor informe outro endereço de email.'))


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(DATA_REQUIRED_LABEL), Email(EMAIL_FIELD_LABEL)])
    submit = SubmitField(_l('Redefinir senha'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('Senha'), validators=[DataRequired(DATA_REQUIRED_LABEL)])
    password2 = PasswordField(_l('Repita a senha'), validators=[DataRequired(DATA_REQUIRED_LABEL), EqualTo('password')])
    submit = SubmitField(_l('Salvar'))
