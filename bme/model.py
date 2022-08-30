
from bme import app, db, loginManager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@loginManager.user_loader
def load_user(userId):
    return User.query.get(int(userId))


#deals with the user and event many to many relationship
user_event = db.Table('user_channel',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)


#Represents the User database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)      #its the primary key
    firstName = db.Column(db.String, nullable=False)    #must not be null
    surName = db.Column(db.String, nullable=False)      #must not be null
    email = db.Column(db.String, nullable=False, unique=True)   #must not be empty, and mun mails are unique
    studentNumber = db.Column(db.String(9), nullable= False, unique=True)      #must not be empty, max of 9 numbers and must be unique
    profilePicture = db.Column(db.String(20), nullable=False, default = 'default.jpg')      #max 20 strings(image will be hashed), cannot be null and some image will always be there i.e. the default image
    password = db.Column(db.String(60), nullable=False)     #passwords will be hashed

    #The user and eventsPosted have a one to many relationship
    eventsPosted = db.relationship('Event', backref='author', lazy=True)        #This is relationship and NOT a column on the db, this just helps get all events the user has created
    #can use the backref, author in this case, to get the user who created the event. So event1.author gives us the user details 

    #all the events the user is attending
    attending = db.relationship('Event', secondary = user_event, backref="atendees", order_by ="Event.date")

    #tokens for password reset
    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'],)
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    #returns the user associated with the token, provided the token hasnt expired
    def verify_reset_token(token, expires_sec=600):            #token expires after 10 mins
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token, expires_sec)['user_id']
        except:  
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.firstName}', '{self.surName}', '{self.studentNumber}', '{self.email}', '{self.profilePicture}')"

#Represents the events database
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(20), nullable=True)      #max 20 strings(image will be hashed), cannot be null and some image will always be there i.e. the default image
    date = db.Column(db.Date, nullable=False)

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.title}', '{self.date}')"

