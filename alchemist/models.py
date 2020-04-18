from alchemist import db,login_manager, git_blueprint, cps_oauth
from flask import flash
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from flask_login import UserMixin, current_user, login_user
from flask_dance.contrib.github import make_github_blueprint
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()



# The user_loader decorator allows flask-login to load the current user
# and grab their id.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    username = db.Column(db.String(64), unique=True, index=True)
    # This connects BlogPosts to a User Author.
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self,  username):
        self.username = username
    def __repr__(self):
        return f"UserName: {self.username}"

class OAuth(OAuthConsumerMixin, db.Model):
    __tablename__= 'OAuth'

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


git_blueprint.storage = SQLAlchemyStorage(OAuth, db.session, user=current_user)


@oauth_authorized.connect_via(git_blueprint)
def git_logged_in(blueprint, token):
    account_info = blueprint.session.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        username = account_info_json['login']


        query = User.query.filter_by(username=username)

        try:
            user = query.one()
        except NoResultFound:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return current_user
class BlogPost(db.Model):
    # Setup the relationship to the User table
    user = db.relationship(User)

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id =user_id


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"
db.create_all()
