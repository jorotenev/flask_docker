import datetime

from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy.orm import backref,validates, subqueryload
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app,session
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.enums import PasswordLength, EmailLength


"""
CONSTANTS
"""
ONE_HOUR_IN_SECONDS = 3600


"""
Model mixins.
"""
class TableWithDatesMixin(object):
    """
    extend this mixin if you want your model to have date columns
    """
    dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    dateUpdated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow(),
                            onupdate=datetime.datetime.utcnow)


class BasicModelMixin(TableWithDatesMixin):
    """
    minimal table mixin. Extend this mixin, together with sqlalchemy's Model
    """
    id = db.Column(db.Integer(), primary_key=True)


"""
Model definitions
"""
class User(BasicModelMixin, UserMixin, db.Model):
    __tablename__ = 'users'

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


    email = db.Column(db.String(50), nullable=False, unique=True, index=True)
    name = db.Column(db.String(30), nullable=False)

    _password = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "[%s]" % self.email


    @validates('email')
    def validate_email(self, column_name, value):
        # validation happens immediately (not on session.commit/flush)
        assert value
        assert column_name == 'email'
        assert len(value) >= EmailLength.MIN and len(value) <= EmailLength.MAX
        assert '@' in value
        return value


    @hybrid_property
    def password(self):
        return self._password


    @password.setter
    def _set_password(self, plaintext):
        # the if is used so we get consistent exception if the field is None
        if plaintext == None:
            self._password = None
        else:
            assert len(plaintext) >= PasswordLength.MIN and len(plaintext) <= PasswordLength.MAX
            self._password = generate_password_hash(plaintext)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

    # flask-login stuff

    # account confirmation
    def generate_confirmation_token(self, expiration=ONE_HOUR_IN_SECONDS):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        token = s.dumps({'confirm': self.id})

        return token

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    # reset password stuff
    @staticmethod
    def generate_reset_pass_token(email, expiration=ONE_HOUR_IN_SECONDS):
        u = User.query.filter_by(email=email).first()
        if u:
            s = Serializer(current_app.config['SECRET_KEY'], expiration)
            return s.dumps({'reset': u.id})
        else:
            raise Exception("No user with such email")

    @staticmethod
    def reset_password_and_get_user(token, new_password, expiration=ONE_HOUR_IN_SECONDS):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        try:
            user_id = s.loads(token).get('reset')
            u = User.query.get(user_id)
            if u:
                u.password = new_password
                db.session.commit()
                return u
            else:
                raise Exception("No user with this id")
        except Exception:
            raise Exception("Invalid token")


class AnonymousUser(AnonymousUserMixin):
    pass


def load_normal_user(user_id):
    """Flask-Login user_loader callback"""
    from app.models import User
    try:
        u = User.query.get(int(user_id))
        return u
    except:
        return None
