from importlib.abc import TraversableResources
import secrets
import os
from bme import app, mail
from flask import url_for, render_template
from PIL import Image
from flask_mail import Message
from flask_login import current_user

#For sending emails to all the attendees when an event is cancelled
def notifyOnEventCancellation(event):
    for attendee in event.atendees:
        sendEmailToAttendee(attendee, event.title, event.date, 2)

#For sending emails to all the attendees when an event is edited/changed
def notifyOnEventEdit(event):
    for attendee in event.atendees:
        sendEmailToAttendee(attendee, event.title, event.date, 1)

#For sending emails to the user when they cancel their booking for an event
def notifyOnBookingCancellation(event):
    sendEmailToAttendee(current_user, event.title, event.date, 3)


#1 for edit
#2 for cancel
def sendEmailToAttendee(attendee, title, date, type):
    if (type==1):
        message = Message('Event Updated', 
                            recipients=[attendee.email])
        message.html = render_template('event_edited.html', firstName = attendee.firstName, eventName = title, date=date)
    if (type==2):
        message = Message('Event cancelled', 
                     
                    recipients=[attendee.email])
        message.html = render_template('event_cancellation.html', firstName = attendee.firstName, eventName = title, date=date)
    if (type==3):
        message = Message('Booking Cancellation', 
                     
                    recipients=[attendee.email])
        message.html = render_template('booking_cancellation.html', firstName = attendee.firstName, eventName = title, date=date)
    mail.send(message)

