# **Book My Event**
>Part of my summer 2022 project. 
>This application was built using Python, Flask, HTML and BootStrap

>Some features of this application include:
- A robust user registration, login and logout feature with proper credential checking 
- Users have the ability to view all events that are posted in an order and oriented manner, with every page showing 5 events
- Users can easily post, edit or delete events
- Users can easily also attend or cancel their attendance for events
- Users can view all the events they are currently attending
- Users can also view all the attendees for an event they created
- Users can view other users and the events posted by them
- Users will receive notifications on their emails for the following events:

    - Successful registration
    
    - Attending an event
    
    - Cancellation their booking for an event
    
    - All the attendees will be notified when the event is edited or deleted
    
  
# Run Configurations
>Only one main change needs to be made - inorder for the emails to be sent, you'd need provide the email credentials on the config.py file. This can be best done using environment variables for security reasons

>Most of the email providers have blocked 3rd part access to emails, so directly inputting your email credentials might not work. In this case you would need to use an "app password" for your email and that should solve it. 
