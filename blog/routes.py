import secrets
import os
from blog import app, db, bcrypt
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from blog.form import RegistrationForm, LoginForm, UpdateAccountForm, PostEventForm, RequestPasswordResetForm, ResetPasswordForm
from blog.model import User, Post
from flask_login import login_user, current_user, logout_user, login_required



#multiple decorators for the same page
@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", posts = posts)


@app.route("/about")
def about():
    return render_template("about.html", title =" - About")


#this route accepts both GET and POST requests now
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    regForm = RegistrationForm()
    #validating the form before returning/posting it
    if regForm.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(regForm.password.data).decode('utf-8')           #hash to string hence the utf-8
        user = User(firstName = regForm.firstName.data, 
                    surName = regForm.surName.data, 
                    studentNumber = regForm.studentNumber.data, 
                    email = regForm.email.data,
                    password = hashedPassword)
        #adds the user to the db
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {regForm.firstName.data}!', 'success')
        login_user(user)
        return redirect(url_for('home'))            #home is the name of the function

    return render_template("register.html", title = "Register", form=regForm)






@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    loginForm = LoginForm()
    #validating the form before returning/posting it
    if loginForm.validate_on_submit():
        user = User.query.filter_by(email = loginForm.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
            login_user(user, remember= loginForm.remember.data)
            nextPage = request.args.get("next")
            if nextPage:
                return redirect(url_for('account'))
            flash(f'Welcome back {user.firstName}!', 'success')
            return redirect(url_for('home'))             #home is the name of the function
        else:
            flash(f'Unsuccessful login - Please try again', 'danger')  
    return render_template("login.html", title = "Login", form=loginForm)






@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))





def saveProfilePicture(formProfilePicture, i):
    randomHex = secrets.token_hex(8)
    _, fExt = os.path.splitext(formProfilePicture.filename)
    profilePictureFn = randomHex + fExt
    #1 for profile pic, 2 for event pic
    if (i==1):
        profilePicturePath = os.path.join(app.root_path, 'static/profilePics', profilePictureFn)
        output_size = (125, 125)
    else:
        profilePicturePath = os.path.join(app.root_path, 'static/postPics', profilePictureFn)
        output_size = (500, 800)

    
    i = Image.open(formProfilePicture)
    i = i.convert("RGB")
    i.thumbnail(output_size)
    i.save(profilePicturePath)

    return profilePictureFn







@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    updateAForm= UpdateAccountForm()

    if updateAForm.validate_on_submit():

        if updateAForm.profilePicture.data:

            profilePictureFile = saveProfilePicture(updateAForm.profilePicture.data, 1)
            current_user.profilePicture = profilePictureFile
            db.session.commit()
            flash("Account has been updated!", "success")
            return redirect(url_for('account'))
            

    profilePic = url_for('static', filename='profilePics/' + current_user.profilePicture)
    return render_template('account.html', title="Account", profilePicture = profilePic, form=updateAForm)






@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def newPost():
    eventForm = PostEventForm()

    if eventForm.validate_on_submit():
        
        post= Post( title=eventForm.title.data, 
                    content = eventForm.description.data, 
                    author=current_user)
    
        if eventForm.image.data:
            eventImageFile = saveProfilePicture(eventForm.image.data, 2)
            post.image = eventImageFile
            db.session.commit()

        db.session.add(post)
        db.session.commit()
        flash("Event has been posted", "success")
        return redirect(url_for('home'))

    return render_template('create_post.html', title="New Post", heading="Post an Event",form =eventForm, post=None)





#<post_id> represents the variable of the post to view i.e.datatype = int
@app.route("/post/<int:post_id>")
@login_required
def viewPost(post_id):

    post = Post.query.get_or_404(post_id) 

    return render_template('view_post.html', title = post.title, post=post)





#<post_id> represents the variable of the post to view i.e.datatype = int
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def editPost(post_id):

    post = Post.query.get_or_404(post_id) 

    if post.author != current_user:
        abort(403) 
    
    updatePostForm = PostEventForm()
    
    if updatePostForm.validate_on_submit():
        post.title = updatePostForm.title.data   
        post.content = updatePostForm.description.data
        if updatePostForm.image.data:
            eventImageFile = saveProfilePicture(updatePostForm.image.data, 2)
            post.image = eventImageFile
        db.session.commit() 
        flash('Your post has been updated!', 'success')
        return redirect(url_for('viewPost', post_id = post.id))

    elif request.method == "GET":
        updatePostForm.title.data = post.title
        updatePostForm.description.data = post.content
            
    return render_template('create_post.html', title="Update Post", heading ="Edit Post", form =updatePostForm, post=post)



#<post_id> represents the variable of the post to view i.e.datatype = int
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def deletePost(post_id):

    post = Post.query.get_or_404(post_id) 

    if post.author != current_user:
        abort(403) 

    db.session.delete(post)
    db.session.commit()

    flash('Your post has been deleted', 'success')
    return redirect(url_for('home'))



#<user_id> represents the variable of the post to view i.e.datatype = int
@app.route("/user/<int:user_id>")
@login_required
def viewUser(user_id):
    page = request.args.get('page', 1, type=int)

    user = User.query.get_or_404(user_id) 
    fullName = "- " +user.firstName + " " +user.surName
    posts = Post.query.filter_by(userId = user_id).order_by(Post.datePosted.desc()).paginate(page=page, per_page=5)

    return render_template('view_user.html', title=fullName, user=user, posts=posts)


#@app.route("/reset", methods=['GET', 'POST'])
#def resetRequest(post_id):

