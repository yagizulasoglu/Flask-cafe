"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from mapping import save_map


bcrypt = Bcrypt()
db = SQLAlchemy()


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = 'cities'

    code = db.Column(
        db.Text,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    state = db.Column(
        db.String(2),
        nullable=False,
    )


class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = 'cafes'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    url = db.Column(
        db.Text,
        nullable=False,
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )

    city_code = db.Column(
        db.Text,
        db.ForeignKey('cities.code'),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-cafe.jpg",
    )

    city = db.relationship("City", backref='cafes')

    def __repr__(self):
        return f'<Cafe id={self.id} name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f'{city.name}, {city.state}'

    def is_liked_by(self, other_user):
        """Is this cafe liked by user?"""

        liked_user_list = [
            user for user in self.users_liked_cafe if user.id == other_user.id]
        return len(liked_user_list) == 1

    def save_map(self):
        """Saves the map image for this cafe."""

        save_map(self.id, self.address, self.city.name, self.city.state)


class Like(db.Model):
    """Cafe likes"""

    __tablename__ = "likes"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        primary_key=True
    )

    cafe_id = db.Column(
        db.Integer,
        db.ForeignKey("cafes.id", ondelete="cascade"),
        primary_key=True
    )


class Speciality(db.Model):
    """Specialties for cafes."""

    __tablename__ = 'specialities'

    name = db.Column(
        db.String(100),
        primary_key=True,
    )

    cafe_id = db.Column(
        db.Integer,
        db.ForeignKey("cafes.id", ondelete="cascade"),
        nullable=False
    )

    cafe = db.relationship("Cafe", backref='specialities')


class User(db.Model):
    """User information"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    admin = db.Column(
        db.Boolean,
        nullable=False
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    description = db.Column(
        db.Text
    )

    image_url = db.Column(
        db.String(255),
        nullable=False,
        default='/static/images/default-pic.jpg',
    )

    password =  db.Column(
        db.String(150),
        nullable=False,
    )

    liked_cafes = db.relationship(
    "Cafe",
    secondary="likes",
    backref="users_liked_cafes"
    )

    def get_full_name(self):
        """Returns a string of full name of the user"""

        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls, username, email, first_name, last_name, description, password, admin=False, image_url='/static/images/default-pic.jpg'):
        """Registers a user, hashes password, and adds user to session."""

        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            admin=admin,
            email=email,
            first_name=first_name,
            last_name=last_name,
            description=description,
            image_url=image_url,
            password=hashed_password,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
