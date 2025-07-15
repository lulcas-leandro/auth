from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

msg_obrigatorio = 'Estre campo é obrigatório.'
msg_senhas_nao_iguais = 'As senhas devem ser iguais.'

class LoginForm(FlaskForm):
    user_name  = StringField('Usuário', validators=[DataRequired(message=msg_obrigatorio)])
    password = PasswordField('Senha', validators=[DataRequired(message=msg_obrigatorio)])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    name = StringField('Nome completo', validators=[DataRequired(message=msg_obrigatorio)])
    user_name = StringField('Nome de Usuário', validators=[DataRequired(message=msg_obrigatorio)])
    password = PasswordField('Senha', validators=[DataRequired(message=msg_obrigatorio)])
    password_confirm = PasswordField(
        'Repita a senha', validators=[DataRequired(message=msg_obrigatorio), EqualTo('password', message=msg_senhas_nao_iguais)])
    submit = SubmitField('Registrar')

    def validate_name(self, user):
        user =  User.query.filter_by(user_name=user.data).first()
        if user is not None:
            raise ValidationError('Esse usuário esta em uso, por favor use outro.')
