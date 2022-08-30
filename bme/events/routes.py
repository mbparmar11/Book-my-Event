from asyncio import events
from bme import db
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from bme.events.form import PostEventForm
from bme.model import  Event
from flask_login import current_user, login_required
from bme.events.utils import notifyOnBookingCancellation, notifyOnEventCancellation, notifyOnEventEdit
from bme.users.utils import saveProfilePicture, checkAttending, sendBookingConfirmationEmail




events = Blueprint('events', __name__)

#app.route becomes blueprint.route

#Route to allow users to create a new event
@events.route("/event/new", methods=['GET', 'POST'])
@login_required
def newEvent():
    form = PostEventForm()

    if form.validate_on_submit():
        
        event= Event( title=form.title.data, 
                    content = form.description.data, 
                    author=current_user,
                    date = form.date.data)
    
        if form.image.data:
            eventImageFile = saveProfilePicture(form.image.data, 2)
            event.image = eventImageFile
            db.session.commit()

        db.session.add(event)
        db.session.commit()
        flash("Event has been posted", "success")
        return redirect(url_for('main.home'))

    return render_template('create_event.html', title="New Event", heading="Post an Event",form =form)



#Route to allow users to view event details where they can attend/cancel booking
#users can also see the list of attendees provided they created that event
#<post_id> represents the variable of the post to view i.e.datatype = int
@events.route("/event/<int:event_id>")
@login_required
def viewEvent(event_id):

    event = Event.query.get_or_404(event_id) 

    return render_template('view_event.html', attending = checkAttending(event), title = event.title, event=event)



#Route for when users opt to attend an event
#<post_id> represents the variable of the post to view i.e.datatype = int
@events.route("/event/<int:event_id>", methods=['GET', 'POST'])
@login_required
def attendEvent(event_id):

    event = Event.query.get_or_404(event_id) 
    event.atendees.append(current_user)

    db.session.commit()
    sendBookingConfirmationEmail(event)
    flash('Thanks for attending, kindly check your email for confirmation', 'success')
    return redirect(url_for('main.home'))


#Route for when user cancels their booking for an event
#<post_id> represents the variable of the post to view i.e.datatype = int
@events.route("/event/<int:event_id>/cancel", methods=['POST'])
@login_required
def removeAttendee(event_id):

    event = Event.query.get_or_404(event_id) 
    current_user.attending.remove(event)
    db.session.commit()

    notifyOnBookingCancellation(event)

    flash('Booking cancelled, kindly check your email for cancellation confirmation', 'success')
    return redirect(url_for('main.home'))




#Route for when a user who created an event, now wants to edit it
#<post_id> represents the variable of the post to view i.e.datatype = int
@events.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def editEvent(event_id):

    event = Event.query.get_or_404(event_id) 

    if event.author != current_user:
        abort(403) 
    
    form = PostEventForm()
    #all the attendees will be notified of the updated details for the event
    if form.validate_on_submit():
        event.title = form.title.data   
        event.content = form.description.data
        if form.image.data:
            eventImageFile = saveProfilePicture(form.image.data, 2)
            event.image = eventImageFile
        db.session.commit() 
        notifyOnEventEdit(event)
        flash('Your event has been updated!', 'success')
        return redirect(url_for('events.viewEvent', event_id = event.id))

    elif request.method == "GET":
        form.title.data = event.title
        form.description.data = event.content
            
    return render_template('create_event.html', title="Update Event", heading ="Edit Event", form =form)


#Route for when a user who created an event, now wants to delete it
#<post_id> represents the variable of the post to view i.e.datatype = int
@events.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def deleteEvent(event_id):

    event = Event.query.get_or_404(event_id) 

#all the attendees will be notified of the event cancellation
    if event.author != current_user:
        abort(403) 
    notifyOnEventCancellation(event)

    db.session.delete(event)
    db.session.commit()

    flash('Your event has been deleted', 'success')
    return redirect(url_for('main.home'))







