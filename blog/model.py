from blog import db, loginManager,app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer

@loginManager.user_loader
def load_user(userId):
    return User.query.get(int(userId))



#Represents the User database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)      #its the primary key
    firstName = db.Column(db.String, nullable=False)    #must not be null
    surName = db.Column(db.String, nullable=False)      #must not be null
    email = db.Column(db.String, nullable=False, unique=True)   #must not be empty, and mun mails are unique
    studentNumber = db.Column(db.String(9), nullable= False, unique=True)      #must not be empty, max of 9 numbers and must be unique
    profilePicture = db.Column(db.String(20), nullable=False, default = 'default.jpg')      #max 20 strings(image will be hashed), cannot be null and some image will always be there i.e. the default image
    password = db.Column(db.String(60), nullable=False)     #passwords will be hashed

    #The user and post have a one to many relationship
    posts = db.relationship('Post', backref='author', lazy=True)        #This is relationship and NOT a column on the db, this just helps get all posts the user has created
    #can use the backref, author in this case, to get the user who created the post. So post1.author gives us the user details 

    #tokens for password reset
    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'],)
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token, expires_sec=600):            #token expires after 10 mins
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token, expires_sec)['user_id']
        except:  
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.firstName}', '{self.surName}', '{self.studentNumber}', '{self.email}', '{self.profilePicture}')"

#Represents the posts database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)      #dateposted is the current time if not provided
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(20), nullable=True)      #max 20 strings(image will be hashed), cannot be null and some image will always be there i.e. the default image


    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.datePosted}')"

