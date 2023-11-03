from flask import Blueprint, flash, request, redirect, url_for, render_template, Response, current_app, jsonify, session
from . import db, bcrypt, login_manager
from apps.models_db import Users
from apps.forms.auth import LoginForm, CreateAccountForm

from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)

from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from werkzeug.routing import BuildError


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = Users.query.filter_by(username=form.username.data).first()
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                road_data_session = session.get('road_data')
    
                if road_data_session:
                    return redirect(url_for('detect.streamcam'))
                return redirect(url_for('views.index'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")
    return render_template('accounts/login.html', 
                           form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = CreateAccountForm()
    if form.validate_on_submit():
        try:
            email = form.email.data
            password = form.password.data
            username = form.username.data

            user = Users.query.filter_by(username=username).first()
            if user:
                flash('Username is not valid or does not exists.', 'danger')
                return redirect(url_for('auth.register'))
            email_check = Users.query.filter_by(email=email).first()
            if email_check:
                flash('Email is not valid or does not exists.', 'danger')
                return redirect(url_for('auth.register'))

            newuser = Users(
                username=username,
                email=email,
                password=password
            )

            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("auth.login"))
    
        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")

    return render_template('accounts/register.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.app_errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403

@auth.app_errorhandler(400)
def handle_bad_request(error):
    return render_template('home/page-403.html'), 400


@auth.app_errorhandler(404)
def page_not_found(error):
    return render_template('home/page-404.html'), 404

@auth.app_errorhandler(405)
def method_not_allow(error):
    return render_template('home/page-403.html'), 405


@auth.app_errorhandler(403)
def handle_cors_error(error):
    return render_template('home/page-403.html'), 403


@auth.app_errorhandler(500)
def internal_server_error(error):
    return render_template('home/page-500.html'), 500
