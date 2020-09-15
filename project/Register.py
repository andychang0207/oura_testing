from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,BooleanField, SubmitField
from wtforms.validators import InputRequired,Length,EqualTo,ValidationError
from project.model import User

def invalid_credentials(form,field):
    username_entered = form.username.data
    password_entered = field.data
    user_object = User.query.filter_by(username = username_entered).first()
    if user_object is None:
        raise ValidationError('username or password is incorrect.')
    elif password_entered != user_object.password:
        raise ValidationError('username or password is incorrect.')

class RegisterForm(FlaskForm):
    username = StringField('',validators=[InputRequired(message='Username required'),Length(min=3,max=15)],
                            render_kw={'placeholder':'Username'})
    password = PasswordField('',validators=[InputRequired(message='Password required'),Length(min=8,max=80)],
                            render_kw={'placeholder':'Password'})
    confirm = PasswordField('',validators=[InputRequired(message='Please repeat your password'),Length(min=8,max=80),EqualTo('password','Password must match')],
                            render_kw={'placeholder':'Repeat your password'})
    submit = SubmitField('Create',render_kw={'class':'btn'})
    def validate_username(self,username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError('Username already exists. Select a different username.')


class LoginForm(FlaskForm):
    username = StringField(label='',validators=[InputRequired(message='Username reqired'), Length(min=3,max=15)],render_kw={'placeholder':'Username'})
    password = PasswordField('',validators=[InputRequired(message='Password required'),invalid_credentials],
                            render_kw={'placeholder':'Password'})
    submit = SubmitField('Log in',render_kw={'class':'btn btn-primary'})