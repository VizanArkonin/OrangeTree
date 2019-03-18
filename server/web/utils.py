"""
Web service utility functions and decorators
"""
import json
from enum import Enum

from flask import Response, request, session
from flask_security import LoginForm

from server.database.models.user.users import Users


class MimeType(Enum):
    """
    Enum for providing mimetypes to Web service response objects
    """
    DEFAULT_MIMETYPE = "text/html"
    JSON_MIMETYPE = "text/json"


class ResponseStatus(Enum):
    """
    Enum for providing status codes to Web service response objects
    """
    OK = 200
    CREATED = 201
    NO_CONTENT = 204

    BAD_REQUEST = 400
    NOT_FOUND = 404
    CONFLICT = 409
    PRECONDITION_FAILED = 412

    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501


class ModifiedLoginForm(LoginForm):
    """
    Modified login form, used instead of flask-security standard form.
    """
    def validate(self):
        # Before-validation code section
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------

        # Validation
        response = super(ModifiedLoginForm, self).validate()

        # After-validation code section
        # --------------------------------------------------------------------------------------------------------------
        user = Users.query.filter(Users.email == request.form['email']).first()
        session['userName'] = "{0} {1}".format(user.first_name, user.last_name)
        # --------------------------------------------------------------------------------------------------------------

        return response


def get_response(content, mimetype=MimeType.DEFAULT_MIMETYPE.value, status=ResponseStatus.OK.value):
    """
    Since return types and data formats may vary, we use this simple wrapper to generate proper response object

    :param content: Content object
    :param mimetype: Mimetype. Consider using MimeType enum for clarity ans consistency
    :param status: HTTP status code. Consider using ResponseStatus enum for clarity and consistency
    :return: Response string or Response object with respective mimetype set
    """
    if isinstance(content, str):
        payload = content
    else:
        payload = json.dumps(content)

    return Response(payload, mimetype=mimetype, status=status)


def process_rest_request(function):
    """
    Decorator, used to cut down the amount of code for try-catch and general conditional branches.
    Used in REST API routes to assert the JSON response status and properly process possible exceptions.

    :return: Response object - from either target function OR from wrapper itself (in case of errors/exceptions).
    """

    def wrap_function(*args, **kwargs):
        try:
            payload = None
            if request.json:
                payload = request.json
                return function(*args, **kwargs)
            else:
                payload["errors"] = ["No json content received"]
                return get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                    status=ResponseStatus.NO_CONTENT.value)
        except Exception as exception:
            if payload:
                payload["errors"] = [exception.args]
                return get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                    status=ResponseStatus.INTERNAL_SERVER_ERROR.value)
            else:
                return get_response({"errors": [exception.args]}, mimetype=MimeType.JSON_MIMETYPE.value,
                                    status=ResponseStatus.BAD_REQUEST.value)

    return wrap_function
