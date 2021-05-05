from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp

from ..models import User, Role


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Real name', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Save changes')


class EditAdminProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp(
            r"^[a-zA-Z]+[a-zA-Z0-9._]*$", 0, 'Username must have only letters, figures, dotts or underscores')
    ])
    email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()
    ])
    role = SelectField('Role', coerce=int)
    confirmed = BooleanField('Confirmed')
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Real name', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Save changes')

    def __init__(self, user, *args, **kwargs):
        super(EditAdminProfileForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.all()]
        self.user = user

    def validate_username(self, field):
        if self.user.username != field.data and User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use')

    def validate_email(self, field):
        if self.user.email != field.data and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered')