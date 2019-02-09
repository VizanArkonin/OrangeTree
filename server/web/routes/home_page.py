"""
Home Page routing library
"""
import json

from flask import request
from flask_login import login_required
from flask_security import roles_accepted
from flask_security.utils import hash_password
from server.database.models.user.roles import Roles

from server.web import db as database
from server.database.models.device.devices import Devices
from server.database.models.device.device_monitor_readings import DeviceSystemMonitorReadings
from server.database.models.user.users import Users
from server.web import web_service, user_datastore
from server.web import utils
from server.socket_server import __server as server
from server.web.utils import ResponseStatus, MimeType, process_rest_request


@web_service.route("/home/getDevicesList", methods=["GET"])
@login_required
@roles_accepted("user", "admin")
def get_devices_list():
    """
    Retrieves a list of all devices, allowed in system

    :return: JSON formatted response
    """
    payload = {"devices": []}
    for device in server.allowed_devices:
        device_data = device.serialize_general_data()
        if server.get_client_by_id(device.device_id):
            device_data["online"] = True
        else:
            device_data["online"] = False

        payload["devices"].append(device_data)

    return utils.get_response(json.dumps(payload), mimetype=MimeType.JSON_MIMETYPE.value)


@web_service.route("/home/validateDeviceExistence", methods=["GET"])
@login_required
@roles_accepted("admin")
def get_device_details():
    """
    Validates if given device exists in the system and returns a simple JSON response, stating true or false.
    Should provide the URL parameter of "device_id", which defines the device to validate.

    Example:
    /home/validateDeviceExistence?device_id=DEV_LITE

    :return: JSON formatted response
    """
    device = server.get_device_by_device_id(request.args.get("device_id"))
    return utils.get_response(
        json.dumps({"deviceExists": True if device else False}),
        mimetype=MimeType.JSON_MIMETYPE.value)


@process_rest_request   # Make sure this decorator goes before routing to prevent namespace_overwrite errors
@web_service.route("/home/device.svc", methods=["POST"])
@login_required
@roles_accepted("admin")
def create_new_device():
    """
    Validates if given device already exists, and if not - creates a new one.
    Request payload should have following format:

    {"deviceData":
        {
        "device_id": "Device ID",
        "device_type": Device Type ID,
        "device_access_key": "Access Key"
        }
    }

    :return: JSON formatted response - request dict with additional List field named "errors".
    """
    payload = request.json
    payload["errors"] = []
    device_id = payload["deviceData"]["device_id"]
    device_type_id = payload["deviceData"]["device_type"]
    device_access_key = payload["deviceData"]["device_access_key"]

    if device_id and device_type_id and device_access_key:
        if not server.get_device_by_device_id(device_id):
            device = Devices()
            device.device_id = device_id
            device.device_type_id = device_type_id
            device.device_access_key = device_access_key
            database.session.add(device)
            database.session.commit()

            server.update_allowed_devices()
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.CREATED.value)
        else:
            payload["errors"] = ["Device with this ID already exists"]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.CONFLICT.value)
    else:
        payload["errors"] = ["One or multiple required fields were empty"]
        return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                  status=ResponseStatus.PRECONDITION_FAILED.value)


@process_rest_request   # Make sure this decorator goes before routing to prevent namespace_overwrite errors
@web_service.route("/home/device.svc", methods=["PUT"])
@login_required
@roles_accepted("admin")
def update_device_details():
    """
    Updates the device definition with provided set of data.
    Request payload should have following format:

    {"deviceData":
        {
        "id": ID,
        "device_id": "Device ID",
        "device_type": Device Type ID,
        "device_access_key": "Access Key"
        }
    }

    :return: JSON formatted response - request dict with additional List field named "errors".
    """
    payload = request.json
    payload["errors"] = []

    db_id = payload["deviceData"]["id"]
    device_id = payload["deviceData"]["device_id"]
    device_type_id = payload["deviceData"]["device_type"]
    device_access_key = payload["deviceData"]["device_access_key"]

    if db_id and device_id and device_type_id:
        device = Devices.query.get(int(db_id))
        if device:
            device.device_id = device_id
            device.device_type_id = device_type_id
            device.device_access_key = device_access_key if device_access_key else device.device_access_key
            database.session.commit()

            server.update_allowed_devices()
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.OK.value)
        else:
            payload["errors"].append("Device with specified ID doesn't exist")
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.CONFLICT.value)
    else:
        payload["errors"] = ["One or multiple required fields were empty"]
        return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                  status=ResponseStatus.PRECONDITION_FAILED.value)


@process_rest_request   # Make sure this decorator goes before routing to prevent namespace_overwrite errors
@web_service.route("/home/device.svc", methods=["DELETE"])
@login_required
@roles_accepted("admin")
def delete_device():
    """
    Validates if given device exists, and if yes - removes it from the database.
    Request payload should have following format:

    {"deviceData":
        {
        "device_id": "Device ID",
        }
    }

    Excessive contents other than device_id field is acceptable - it's just not going to be processed

    :return: JSON formatted response - request dict with additional List field named "errors".
    """
    payload = request.json
    payload["errors"] = []
    device_id = payload["deviceData"]["device_id"]

    if device_id:
        if server.get_device_by_device_id(device_id):
            device = Devices.query.filter(Devices.device_id == device_id)
            # Since system monitor logs are detached from Device model - we delete it first, separately
            DeviceSystemMonitorReadings.query.filter(
                DeviceSystemMonitorReadings.device_id == device.first().id).delete()
            # Once done - we delete device with it's included dependencies
            device.delete()
            database.session.commit()

            server.update_allowed_devices()
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.OK.value)
        else:
            payload["errors"] = ["Device with this ID doesn't exist."]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.NOT_FOUND.value)
    else:
        payload["errors"] = ["One or multiple required fields were empty"]
        return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                  status=ResponseStatus.PRECONDITION_FAILED.value)


@web_service.route("/home/getUsersList", methods=["GET"])
@login_required
@roles_accepted("user", "admin")
def get_users_list():
    """
    Retrieves a list of all users, registered in the system
    :return: :return: JSON formatted response
    """
    return utils.get_response(
        json.dumps({"users": [user.serialize_general_data() for user in Users.query.all()]}),
        mimetype=MimeType.JSON_MIMETYPE.value)


@web_service.route("/home/getUserRolesList", methods=["GET"])
@login_required
@roles_accepted("user", "admin")
def get_users_roles_list():
    """
    Retrieves a list of all user roles
    :return: :return: JSON formatted response
    """
    return utils.get_response(
        json.dumps({"userRoles": [role.serialize() for role in Roles.query.all()]}),
        mimetype=MimeType.JSON_MIMETYPE.value)


@web_service.route("/home/validateUserExistence", methods=["GET"])
@login_required
@roles_accepted("admin")
def get_user_details():
    """
    Validates if given user exists in the system and returns a simple JSON response, stating true or false.
    Should provide URL parameter of "user_email", which will define the user to validate.

    Example:
    /home/validateUserExistence?user_email=some@mail.com

    :return: JSON formatted response
    """
    user = Users.query.filter(Users.email == request.args.get("user_email")).first()
    return utils.get_response(
        json.dumps({"userExists": True if user else False}),
        mimetype=MimeType.JSON_MIMETYPE.value)


@process_rest_request   # Make sure this decorator goes before routing to prevent namespace_overwrite errors
@web_service.route("/home/user.svc", methods=["POST"])
@login_required
@roles_accepted("admin")
def create_user():
    """
    Validates if given user already exists, and if not - creates a new one.
    Request payload should have following format:

    {"userData":
        {
        "email": "User email",
        "password": "User password",
        "first_name": "First Name",
        "last_name": "Last Name",
        "active": True/False,
        "roles":
            [
                {"role_name": "Role string"}
            ]
        }
    }

    :return: JSON formatted response - request dict with additional List field named "errors".
    """
    payload = request.json
    payload["errors"] = []
    user_email = payload["userData"]["email"]
    user_password = payload["userData"]["password"]
    user_first_name = payload["userData"]["first_name"]
    user_last_name = payload["userData"]["last_name"]
    user_active = payload["userData"]["active"]

    if user_email and user_password and user_first_name and user_last_name:
        user = Users.query.filter(Users.email == user_email).first()
        if not user:
            roles_to_add = []
            for role_requested in payload["userData"]["roles"]:
                role_name = role_requested["role_name"]
                db_role_instance = user_datastore.find_role(role_name)
                if db_role_instance:
                    roles_to_add.append(role_name)
            user = user_datastore.create_user(email=user_email,
                                              password=hash_password(user_password),
                                              roles=roles_to_add)
            user.first_name = user_first_name
            user.last_name = user_last_name
            user.active = bool(user_active)
            database.session.commit()

            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.CREATED.value)
        else:
            payload["errors"] = ["User with this email already exists"]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.CONFLICT.value)
    else:
        payload["errors"] = ["One or multiple required fields were empty"]
        return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                  status=ResponseStatus.PRECONDITION_FAILED.value)


@process_rest_request   # Make sure this decorator goes before routing to prevent namespace_overwrite errors
@web_service.route("/home/user.svc", methods=["PUT"])
@login_required
@roles_accepted("admin")
def update_user():
    """
    Updates existing user.
    Request payload should have following format:

    {"userData":
        {
        "id": User ID,
        "email": "User email",
        "password": "User password",
        "first_name": "First Name",
        "last_name": "Last Name",
        "active": True/False,
        "roles":
            [
                {"role_name": "Role string"}
            ]
        }
    }

    :return: JSON formatted response - request dict with additional List field named "errors".
    """
    payload = request.json
    payload["errors"] = []

    user_id = payload["userData"]["id"]
    user_email = payload["userData"]["email"]
    user_password = payload["userData"]["password"]
    user_first_name = payload["userData"]["first_name"]
    user_last_name = payload["userData"]["last_name"]
    user_active = payload["userData"]["active"]

    if user_id and user_email and user_first_name and user_last_name:
        user = Users.query.get(int(user_id))
        if user:
            requested_roles = [role["role_name"] for role in payload["userData"]["roles"]]
            existing_roles = [role.name for role in user.roles]
            if not requested_roles == existing_roles:
                for existing_role in existing_roles:
                    user_datastore.remove_role_from_user(user.email, existing_role)

            for requested_role in requested_roles:
                user_datastore.add_role_to_user(user.email, requested_role)

            if user_password:
                user.password = hash_password(user_password)

            user.email = user_email
            user.first_name = user_first_name
            user.last_name = user_last_name
            user.active = bool(user_active)

            database.session.commit()

            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.OK.value)
        else:
            payload["errors"] = ["User with this ID doesn't exist"]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.CONFLICT.value)
    else:
        payload["errors"] = ["One or multiple required fields were empty"]
        return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                  status=ResponseStatus.PRECONDITION_FAILED.value)


@process_rest_request   # Make sure this decorator goes before routing to prevent namespace_overwrite errors
@web_service.route("/home/user.svc", methods=["DELETE"])
@login_required
@roles_accepted("admin")
def delete_user():
    """
    Validates if given user exists, and if yes - removes it from the database.
    Request payload should have following format:

    {"userData":
        {
            "email": "User email",
        }
    }

    Excessive contents other than email field is acceptable - it's just not going to be processed

    :return: JSON formatted response - request dict with additional List field named "errors".
    """
    payload = request.json
    payload["errors"] = []
    user_email = payload["userData"]["email"]
    if user_email:
        user = Users.query.filter(Users.email == user_email).first()
        if user:
            user_datastore.delete_user(user)

            database.session.commit()

            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.OK.value)
        else:
            payload["errors"] = ["User with this email doesn't exist"]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.CONFLICT.value)
    else:
        payload["errors"] = ["One or multiple required fields were empty"]
        return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                  status=ResponseStatus.PRECONDITION_FAILED.value)
