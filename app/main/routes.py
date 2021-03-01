"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from app.models import Player, Team, Coach, User
# from app.main.forms import BookForm, AuthorForm, GenreForm
from app import bcrypt

# Import app and db from events_app package so that we can run app
from app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    all_users = User.query.all()
    return render_template('home.html', all_users=all_users)
