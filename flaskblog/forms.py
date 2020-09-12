from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError 
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2,20)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2,20)])
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(2,20)])
    facebook = StringField('Facebook', validators=[DataRequired(), Length(2,60)])
    twitter = StringField('Twitter', validators=[DataRequired(), Length(2,60)])

    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg','png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')    

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Category', choices=[('General','General'),('Sports','Sports'),('Gaming','Gaming'),('News','News'),('TV','TV'),
                                                ('Memes','Memes'),('Travel','Travel'),('Music, Art & Design','Music, Art & Design')])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired(), Length(3,800)])
    submit = SubmitField('Comment')

class CategoryForm(FlaskForm):
    category = SelectField('Category', choices=[('All','All'),('General','General'),('Sports','Sports'),('Gaming','Gaming'),('News','News'),('TV','TV'),
                                            ('Memes','Memes'),('Travel','Travel'),('Music, Art & Design','Music, Art & Design')])
    submit = SubmitField('Apply')