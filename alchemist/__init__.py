import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.github import make_github_blueprint, github
from flask_admin import Admin

##############
###GIT HUB####
##Login Setup#
##############


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
########################
#### app ####
##########


app = Flask(__name__)




#############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ###############
###########################################################################

# Remember you need to set your environment variables at the command line
# when you deploy this to a real website.
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret
app.config['SECRET_KEY'] = 'mysecret'

#################################
### DATABASE SETUPS ############
###############################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vprduixzljeqwx:c1f9fa6cb11261818a2b0db8465f6d3e64e7a6573691d5911465b587deec0d8f@ec2-52-6-143-153.compute-1.amazonaws.com:5432/ddaf86bk4q3bdj'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"


######################################
###### OAuth for GIT HUB & GOOGLE ####
######################################
git_blueprint = make_github_blueprint(
    client_id="b144573e0f78b157baf4",
    client_secret="91b1db4f6f1aebe6cf0837b7b0496bb6465c5e87",
)
##############################
######### flask_admin#########
##############################






###########################
#### BLUEPRINT CONFIGS #######
#########################

# Import these at the top if you want
# We've imported them here for easy reference
from alchemist.core.views import core
from alchemist.users.views import users
from alchemist.blog_posts.views import blog_posts
from alchemist.error_pages.handlers import error_pages

# Register the apps
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(git_blueprint, url_prefix="/login")
