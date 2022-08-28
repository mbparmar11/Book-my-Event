from asyncio import events
from blog import db
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from blog.events.form import PostEventForm
from blog.model import  Event
from flask_login import current_user, login_required
from blog.events.utils import notifyOnBookingCancellation, notifyOnEventCancellation, notifyOnEventEdit
from blog.users.utils import saveProfilePicture, checkAttending, sendBookingConfirmationEmail




events = Blueprint('events', __name__)

#app.route becomes blueprint.route

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




#<post_id> represents the variable of the post to view i.e.datatype = int
@events.route("/event/<int:event_id>")
@login_required
def viewEvent(event_id):

    event = Event.query.get_or_404(event_id) 

    return render_template('view_event.html', attending = checkAttending(event), title = event.title, event=event)




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





#<post_id> represents the variable of the post to view i.e.datatype = int
@events.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def editEvent(event_id):

    event = Event.query.get_or_404(event_id) 

    if event.author != current_user:
        abort(403) 
    
    form = PostEventForm()
    
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



#<post_id> represents the variable of the post to view i.e.datatype = int
@events.route("/event/<int:event_id>/delete", methods=['POST'])
@login_required
def deleteEvent(event_id):

    event = Event.query.get_or_404(event_id) 

    if event.author != current_user:
        abort(403) 
    notifyOnEventCancellation(event)

    db.session.delete(event)
    db.session.commit()

    flash('Your event has been deleted', 'success')
    return redirect(url_for('main.home'))







