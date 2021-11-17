from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from werkzeug.wrappers import request
from models import connect_db, db, User, Feedback, authorize
from forms import NewUserForm, LoginForm, EditFeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def show_home():
    """ Send user to /register to create a login """

    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_new_user():
    """ Show and process registration form for new users """
    form = NewUserForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """ Show and process login form for registered users """
    form = LoginForm()
     
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if User.authenticate(username, password):
            # successful login
            session['username'] = username
            return redirect(f'/users/{username}')

        else:
            # re-render the login page with an error
            form.username.errors = ["Username and/or password incorrect"]

    return render_template("login.html", form=form)

@app.route('/users/<username>')
def show_user_info(username):
    """ Show information about a user """

    if 'username' in session:
        user = User.query.filter_by(username=username).first()
        feedback = Feedback.query.filter_by(username=user.username).all()

        return render_template('user_details.html', user=user, feedback=feedback)

    else:
        flash('Please login to view user details', 'danger')
        return redirect('/login')


@app.route('/users/<username>/delete', methods=['GET', 'POST'])
def delete_user(username):
    """ Delete user and all feedback from database """
    user = User.query.get(username)
    users_feedback = Feedback.query.filter_by(username=user.username).all()

    if authorize(username):
        db.session.delete(user)
        for feedback in users_feedback:
            db.session.delete(feedback)
        db.session.commit()
        session.pop('username')
        return redirect('/')

    else:
        flash(f'You are not authorized to delete {username}','danger')
        return redirect('/users/<username>')
    

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    """ Show and process add feedback form """
    user = User.query.get(username)
    form = EditFeedbackForm()

    if authorize(username):
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            new_feedback = Feedback(username=username, title=title, content=content)

            db.session.add(new_feedback)
            db.session.commit()

            return redirect(f'/users/{user.username}')

        else:
            return render_template('add_feedback.html', form=form)

    else:
        flash(f'You are not authorized to add feedback for {username}','danger')
        return redirect('/users/<username>')


@app.route('/feedback/<feedback_id>/update', methods=['GET','POST'])
def edit_feedback(feedback_id):
    """ Show and process feedback edit form """
    feedback = Feedback.query.get(feedback_id)
    user = User.query.filter_by(username=feedback.username).first()
    form = EditFeedbackForm(obj=feedback)

    if authorize(feedback.username):
        if form.validate_on_submit():         
            feedback.title = form.title.data
            feedback.content = form.content.data

            db.session.add(feedback)
            db.session.commit()

            return redirect(f'/users/{user.username}')

        else:
            return render_template('edit_feedback.html', form=form)

    else:
        flash(f'You are not authorized to edit feedback written by {feedback.username}.', 'danger')
        return redirect(f'/users/{user.username}')


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """ Delete a feedback item """
    feedback = Feedback.query.get(feedback_id)

    if authorize(feedback.username):
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')

    else:
        flash(f'You are not authorized to delete that feedback', 'danger')
        return redirect(f'/users/{feedback.username}')


@app.route('/logout')
def logout():
    """ Clear session cookie """

    if 'username' in session:
        session.pop('username')
        flash(f'User logged out', 'success')

    return redirect('/')
