"""Flask App for Flask Cafe."""

import os
from dotenv import load_dotenv

from flask import Flask, render_template, flash, redirect, session, g, jsonify, request
#from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import CafeInfoForm, SignupForm, LoginForm, CsrfForm, ProfileEditForm
from models import connect_db, Cafe, db, City, User, Like

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///flask_cafe')
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')

if app.debug:
    app.config['SQLALCHEMY_ECHO'] = True

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

#toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

@app.before_request
def form_protection():
    """Creates Csrf form protection"""

    g.csrf_form = CsrfForm()

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def get_cities_choices():
    """Gets all cities' ids and name from the database"""

    cities = City.query.all()
    return [(city.code, city.name) for city in cities]

#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")

@app.errorhandler(404)
def not_found_error(error):
    """Returns 404.html when 404 error occurs."""

    return render_template('404.html')
#######################################
# user


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    do_logout()

    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                username=form.username.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                description=form.description.data,
                email=form.email.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            flash("You are signed up and logged in.", 'success')
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('auth/signup-form.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('auth/signup-form.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data,
        )

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials", 'danger')

    return render_template('auth/login-form.html', form=form)


@app.post('/logout')
def logout():
    """Handle logout of user and redirect to homepage."""

    if not g.csrf_form.validate_on_submit() or not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    flash("successfully logged out", "success")
    do_logout()
    return redirect("/")


#######################################
# cafes


@app.get('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.get('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )


@app.route('/cafes/add', methods=["GET", "POST"])
def add_cafe():
    """Shows the form for adding a cafe and if the credentials
    are valid on submit, adds the cafe.
    """

    if not g.user or not g.user.admin:
        flash("Not authorized", "danger")
        return redirect("/login")

    form = CafeInfoForm()
    form.city_code.choices = get_cities_choices()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        url = form.url.data
        address = form.address.data
        city_code = form.city_code.data
        image_url = form.image_url.data

        cafe = Cafe(name=name, description=description, url=url,
                    address=address, city_code=city_code, image_url=image_url)

        db.session.add(cafe)
        db.session.commit()

        flash(f"{cafe.name} added.")
        return redirect (f'/cafes/{cafe.id}')

    else:
        return render_template('cafe/add-form.html', form=form)

@app.route('/cafes/<int:cafe_id>/edit', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    """Shows the form for editing a cafe and if the credentials
    are valid on submit, edits the cafe.
    """

    if not g.user or not g.user.admin:
        flash("Not authorized", "danger")
        return redirect("/login")

    cafe = Cafe.query.get_or_404(cafe_id)
    form = CafeInfoForm(obj=cafe)
    form.city_code.choices = get_cities_choices()

    if form.validate_on_submit():
        city_code = form.city_code.data
        form.populate_obj(cafe)
        cafe.city_code = city_code

        db.session.commit()

        flash(f"{cafe.name} edited.")
        return redirect (f'/cafes/{cafe.id}')

    else:
        return render_template('cafe/edit-form.html', form=form, cafe=cafe)


##############################
#Profile

@app.get('/profile')
def get_profile():
    """Shows profile page."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/")
    g.user_id = g.user.id
    user = User.query.get_or_404(g.user_id)

    return render_template('profile/detail.html', user=user)

@app.route('/profile/edit', methods=["GET", "POST"])
def profile():
    """Update profile for current user."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/")

    form = ProfileEditForm(obj=g.user)

    if form.validate_on_submit():
        form.populate_obj(g.user)
        flash('Profile edited.', "danger")
        return redirect("/profile")
    else:
        return render_template("profile/edit-form.html", form=form)

@app.get('/api/likes')
def likes():
    """figures out if the current user likes that cafe,
    and returns JSON: {"likes": true|false}. If the user is not logged in,
    returns JSON {"error": "Not logged in"}.
    """

    if not g.user:
        return jsonify({"error": "Not logged in"}), 400

    cafe_id = request.args.get('cafe_id')
    print(cafe_id)

    liked = Like.query.filter_by(user_id=g.user.id, cafe_id=cafe_id).first()

    return jsonify({"likes": bool(liked)})

@app.post('/api/like')
def like():
    """makes the current user like a cafe. Return JSON {"liked": cafe_id}
    If the user is not logged in, returns JSON {"error": "Not logged in"}.
    """
    breakpoint()
    if not g.user:
        return jsonify({"error": "Not logged in"}), 400


    cafe_id = request.json['cafe_id']
    cafe = Cafe.query.get_or_404(cafe_id)

    g.user.liked_cafes.append(cafe)
    db.session.commit()

    return jsonify({"liked": cafe_id})


@app.post('/api/unlike')
def unlike():
    """makes the current user unlike cafe #1. Return JSON {"unliked": cafe_id}
    If the user is not logged in, returns JSON {"error": "Not logged in"}.
    """

    if not g.user:
        return jsonify({"error": "Not logged in"}), 400


    cafe_id = request.json['cafe_id']

    Like.query.filter_by(user_id=g.user.id, cafe_id=cafe_id).delete()
    db.session.commit()

    return jsonify({"unliked": cafe_id})