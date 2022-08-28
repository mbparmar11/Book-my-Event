from importlib.abc import TraversableResources
import secrets
import os
from blog import app, mail
from flask import url_for, render_template
from PIL import Image
from flask_mail import Message
from flask_login import current_user




def saveProfilePicture(formProfilePicture, i):
    randomHex = secrets.token_hex(8)
    _, fExt = os.path.splitext(formProfilePicture.filename)
    profilePictureFn = randomHex + fExt
    #1 for profile pic, 2 for event pic
    if (i==1):
        profilePicturePath = os.path.join(app.root_path, 'static/profilePics', profilePictureFn)
        output_size = (125, 125)
    else:
        profilePicturePath = os.path.join(app.root_path, 'static/eventPics', profilePictureFn)
        output_size = (500, 800)

    
    i = Image.open(formProfilePicture)
    i = i.convert("RGB")
    i.thumbnail(output_size)
    i.save(profilePicturePath)

    return profilePictureFn


#sends a welcome email on successful registration
def sendWelcomeEmail(user):
    message = Message('Welcome to Book my Seminar!', 
                        sender = "kehammakene@gmail.com", 
                        recipients=[user.email])
    message.body = f'''Hey there and thanks for registering
'''
    mail.send(message)








#           RESET PASSWORD METHODS          #

#Sends the email to reset the user's password
def sendResetPasswordEmail(user):
    token = user.get_reset_token()
    message = Message('Password Reset', 
                        sender = "help@nono.com", 
                        recipients=[user.email])
    message.body = f'''To reset your password, visit the following link:
{url_for('users.resetPassword', token=token, _external=True)}

If you did not make this request then kindly simply ignore this email.
'''
    mail.send(message)


#Sends the email on an event booking
def sendBookingConfirmationEmail(event):
    message = Message('Booking confirmed', 
                        sender = "help@nono.com", 
                        recipients=[current_user.email])

    message.html = render_template('confirmation_email.html', name = current_user.firstName, eventName = event.title, organizerFirstName = event.author.firstName, organizerSurName= event.author.surName, date=event.date  )
    mail.send(message)


#checks if user is already attending the event 
def checkAttending(eventToCheck):
    for event in current_user.attending:
        if event is eventToCheck:
            return True
    return False


