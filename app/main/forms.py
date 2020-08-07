from flask import request
from flask_babel import _, lazy_gettext as _l
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length

from app.models import User

DATA_REQUIRED_LABEL = 'Esse campo é obrigatório!'
MAX_LENGTH_LABEL = 'Esse campo pode conter no máximo %i caracteres!'
EQUAL_FIELD_LABEL = 'O valor desse campo deve ser igual ao do campo %s!'
EMAIL_FIELD_LABEL = 'O valor desse campo deve ser um endereço de email válido!'


class EditProfileForm(FlaskForm):
    username = StringField(_l('Usuário'), validators=[DataRequired(), Length(max=64, message=MAX_LENGTH_LABEL % 64)])
    about_me = TextAreaField(_l('Sobre mim'), validators=[
        Length(min=0, max=500, message=MAX_LENGTH_LABEL % 500)])
    submit = SubmitField(_l('Salvar'))

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                raise ValidationError(_('Por favor escolha um nome de usuário diferente'))


class EmptyForm(FlaskForm):
    submit = SubmitField()


class PostForm(FlaskForm):
    # __searchable__ = ['body']
    post = TextAreaField(_l('Diga algo'), validators=[DataRequired(DATA_REQUIRED_LABEL),
                                                      Length(max=500, message=MAX_LENGTH_LABEL % 500)])
    submit = SubmitField(_l('Postar'))


class SearchForm(FlaskForm):
    q = StringField(_l('Pesquisar'), validators=[DataRequired(DATA_REQUIRED_LABEL)])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Mensagem'), validators=[DataRequired(DATA_REQUIRED_LABEL), Length(max=500)])
    submit = SubmitField(_l('Enviar'))
