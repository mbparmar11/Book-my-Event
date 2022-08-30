from flask import render_template, request
from bme.model import Event
from flask_login import login_required




from flask import Blueprint

main = Blueprint('main', __name__)

#app.route becomes blueprint.route

#This rperesents the home route, showing the home page
#multiple decorators for the same page
@main.route("/")
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.id.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", events = events, showSidePanel=True)

