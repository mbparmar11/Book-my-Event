from bme.model import User
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError




#The user registration fomr
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


#Form allowing users to update their account
#Only profile pictures can be changed, as names, student number and mun email addresses are fixed
class UpdateAccountForm(FlaskForm):

    profilePicture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField("Update Account Details")

#when the user clicks the forgot password button, this form will show asking for their email.
class RequestPasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])          #send reset instructions to the email
    submit = SubmitField("Request Password Reset")

#the user is taken to a diff page where this form is shown, user is asked to provide their email address inorder to request a password reset
    
    #checking if an account with the inputted email even exists in the first place
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()                     #email.data comes from the form
        if user is None:
            raise ValidationError("No account with this email")

#The form allowing the user to now input their new password. This form opens via a link from the user's email
class ResetPasswordForm(FlaskForm):

    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    passwordConfirmation = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    
    submit = SubmitField("Reset Password")
