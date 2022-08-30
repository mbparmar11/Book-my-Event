
import os

class Config:

    SECRET_KEY = "17b65ec1ce5b91a8c73e39e04e56f80ba2cda099"         #added to environment variables for security purposes
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'                   #added to environment variables for security purposes
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME= #YOUR EMAIL ADDRESS                         #added to environment variables for security purposes
    MAIL_PASSWORD = #YOUR PASSWORD                              #added to environment variables for security purposes 
    MAIL_DEFAULT_SENDER = #YOUR EMAIL ADDRESS                   #specifies the default sender, so no need to define the sender when sending the emails