from bme import db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from bme.users.form import RegistrationForm, LoginForm, UpdateAccountForm, RequestPasswordResetForm, ResetPasswordForm
from bme.model import User, Event
from flask_login import login_user, current_user, logout_user, login_required
from bme.users.utils import saveProfilePicture, sendResetPasswordEmail, sendWelcomeEmail

from flask import Blueprint


users = Blueprint('users', __name__)

#only contains route specific to the users blueprint

#app.route becomes blueprint.route
#this route accepts both GET and POST requests now
@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    regForm = RegistrationForm()
    #validating the form before returning/posting it
    if regForm.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(regForm.password.data).decode('utf-8')           #hash to string hence the utf-8
        user = User(firstName = regForm.firstName.data, 
                    surName = regForm.surName.data, 
                    studentNumber = regForm.studentNumber.data, 
                    email = regForm.email.data,
                    password = hashedPassword)
        #adds the user to the db
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {regForm.firstName.data}!', 'success')
        login_user(user)
    
        sendWelcomeEmail(user)        
    
        return redirect(url_for('main.home'))            #home is the name of the function

    return render_template("register.html", title = "Register", form=regForm)




#For user login
@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    loginForm = LoginForm()
    #validating the form before returning/posting it
    if loginForm.validate_on_submit():
        user = User.query.filter_by(email = loginForm.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
            login_user(user, remember= loginForm.remember.data)
            nextPage = request.args.get("next")

            if nextPage:
                return redirect(nextPage)
            flash(f'Welcome back {user.firstName}!', 'success')
            return redirect(url_for('main.home'))             #home is the name of the function
        else:
            flash(f'Unsuccessful login - Please try again', 'danger')  
    return render_template("login.html", title = "Login", form=loginForm)





#For user logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))



#Allows the user to view their account, also allowing them to update their account
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    updateAForm= UpdateAccountForm()

    if updateAForm.validate_on_submit():

        if updateAForm.profilePicture.data:

            profilePictureFile = saveProfilePicture(updateAForm.profilePicture.data, 1)
            current_user.profilePicture = profilePictureFile
            db.session.commit()
            flash("Account has been updated!", "success")
            return redirect(url_for('users.account'))
            

    page = request.args.get('page', 1, type=int)
    eventsPosted = Event.query.filter_by(userId = current_user.id).order_by(Event.date.desc()).paginate(page=page, per_page=5)

    profilePic = url_for('static', filename='profilePics/' + current_user.profilePicture)
    return render_template('account.html', title="Account", user= current_user, profilePicture = profilePic, form=updateAForm, eventsPosted = eventsPosted)



#To view another user, by clikcing on their name from their post on the home screen
@users.route("/user/<int:user_id>")
@login_required
def viewUser(user_id):
    page = request.args.get('page', 1, type=int)

    user = User.query.get_or_404(user_id) 
    fullName = "- " +user.firstName + " " +user.surName
    eventsPosted = Event.query.filter_by(userId = user_id).order_by(Event.date.desc()).paginate(page=page, per_page=5)

    return render_template('view_user.html', title=fullName, user=user, eventsPosted=eventsPosted)



#When user's click the forgot password? button on the login page.
#User enters their email where reset instructions will be sent
@users.route("/reset", methods=['GET', 'POST'])
def requestPasswordReset():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestPasswordResetForm()

    #get the user who wants to reset their password, using the email provided on their request form
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sendResetPasswordEmail(user)
        flash('Please check your email to reset your password - this should be done within 10 minutes', 'info')
        return redirect(url_for('users.login'))


    return render_template('reset_request.html', title="Reset Password", form=form)


#to reset the password - must be done within 10 minutes for requesting the reset
@users.route("/reset/<token>", methods=['GET', 'POST'])
def resetPassword(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)       #returns the User associated with the token, provided the token hasnt expired

    #if not done within 10 mins
    if user is None:
        flash('Invalid/Expired token. Kindly retry again!', 'warning')
        return redirect(url_for('users.requestPasswordReset'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')           #hash to string hence the utf-8
        user.password = hashedPassword        
        db.session.commit()
        flash(f'Password has been reset!', 'success')
        return redirect(url_for('users.login'))            #home is the name of the function

    return render_template('reset_password.html', title="Reset Password", form=form)


#Allows users to see which events they are attending
@users.route("/attending", methods=['GET', 'POST'])
@login_required
def viewAttendingEvents():

    return render_template('view_attending.html', title="Attending")
