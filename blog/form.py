from tokenize import String
from blog.model import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


#every form name is represented as a class
#so this represents the registration form

class RegistrationForm(FlaskForm):

    firstName = StringField("First Name", validators = [DataRequired()])
    surName = StringField("Surname", validators = [DataRequired()])
    studentNumber = StringField("Student Number", validators = [DataRequired(), Length(min =9, max=9)])
    email = StringField("Mun mail", validators = [DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    passwordConfirmation = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Register")

    def validate_studentNumber(self, studentNumber):
        user = User.query.filter_by(studentNumber = studentNumber.data).first()     #studentNumber.data comes from the form
        if user:
            raise ValidationError("Account with this student number already exists")
   
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()                     #email.data comes from the form
        if user:
            raise ValidationError("Account with this email already exists")



#This now represents a Login form
class LoginForm(FlaskForm):

    email = StringField("Email", validators = [DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    #allows users to stay logged in after some time the browser closes
    remember = BooleanField("Remember Me")
    
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):

    profilePicture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField("Update Account Details")



class PostEventForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    image = FileField("Add/Change Poster", validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField("Post Event")


class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()                     #email.data comes from the form
        if user is None:
            raise ValidationError("No account with this email")


class ResetPasswordForm(FlaskForm):

    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    passwordConfirmation = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    
    submit = SubmitField("Reset Password")
