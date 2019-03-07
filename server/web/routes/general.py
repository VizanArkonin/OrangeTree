"""
General routing library
"""

from flask import render_template, redirect, url_for
from flask_login import user_logged_in
from flask_security import login_required, roles_accepted, logout_user
from datetime import datetime

from server.web import web_service


@user_logged_in.connect_via(web_service)
def on_user_logged_in(sender, user):
    """
    This function is fired after user have been successfully logged in.

    :param sender: Sender instance (Flask)
    :param user: User instance
    :return: None
    """
    user.last_login_at = datetime.now()
    if user.login_count:
        user.login_count += 1
    else:
        user.login_count = 1


@web_service.errorhandler(404)
def not_found(e):
    """
    Default error handler for 404 NOT-FOUND HTTP code

    :param e: Error
    :return: Rendered template
    """
    return render_template("service/not_found.html"), 404


@web_service.route("/index", methods=["GET"])
@login_required
@roles_accepted("user", "admin")
def index():
    """
    Maps monitor path to a static index file
    :return: Rendered template
    """
    return render_template("general/index.html")


@web_service.route("/", methods=["GET"])
def empty_index_redirect():
    """
    Redirect route for simply forward-slash address, which should refer to index
    :return: Redirect instance
    """
    return redirect(url_for("index"))


@web_service.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
