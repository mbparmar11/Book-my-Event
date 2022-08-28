from importlib.abc import TraversableResources
import secrets
import os
from blog import app, mail
from flask import url_for, render_template
from PIL import Image
from flask_mail import Message
from flask_login import current_user

def notifyOnEventCancellation(event):
    for attendee in event.atendees:
        sendEmailToAttendee(attendee, event.title, event.date, 2)


def notifyOnEventEdit(event):
    for attendee in event.atendees:
        sendEmailToAttendee(attendee, event.title, event.date, 1)

def notifyOnBookingCancellation(event):
    sendEmailToAttendee(current_user, event.title, event.date, 3)


#1 for edit
#2 for cancel
def sendEmailToAttendee(attendee, title, date, type):
    if (type==1):
        message = Message('Event Updated', 
                            sender = "help@nono.com", 
                            recipients=[attendee.email])
        message.html = render_template('event_edited.html', firstName = attendee.firstName, eventName = title, date=date)
    if (type==2):
        message = Message('Event cancelled', 
                    sender = "help@nono.com", 
                    recipients=[attendee.email])
        message.html = render_template('event_cancellation.html', firstName = attendee.firstName, eventName = title, date=date)
    if (type==3):
        message = Message('Booking Cancellation', 
                    sender = "help@nono.com", 
                    recipients=[attendee.email])
        message.html = render_template('booking_cancellation.html', firstName = attendee.firstName, eventName = title, date=date)
    mail.send(message)

