"""
Home Page routing library
"""
import json

from flask import request
from flask_login import login_required
from flask_security import roles_accepted

from database import db_session
from database.models.device import DevicesList
from web import web_service, utils
from board_controller.server import __server as server
from web.utils import ResponseStatus, MimeType


@web_service.route("/home/getDevicesList", methods=["GET"])
@login_required
@roles_accepted("user", "admin")
def getDevicesList():
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


@web_service.route("/home/getDeviceDetails/<int:device_id>", methods=["GET"])
@login_required
@roles_accepted("user", "admin")
def getDeviceDetails(device_id):
    """
    Retrieves all data for given device, packs it in JSON and returns a response

    :param device_id: Device ID
    :return: JSON formatted response
    """
    device = server.get_device_by_id(device_id)
    return utils.get_response(
        json.dumps({"deviceData": device.serialize_all() if device else {}}),
        mimetype=MimeType.JSON_MIMETYPE.value)


@web_service.route("/home/device.svc", methods=["POST"])
@login_required
@roles_accepted("user", "admin")
def createNewDevice():
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
    try:
        payload = None
        if request.json:
            payload = request.json
            device_id = payload["deviceData"]["device_id"]
            if not server.get_device_by_device_id(device_id):
                device = DevicesList()
                device.device_id = device_id
                device.device_type = payload["deviceData"]["device_type"]
                device.device_access_key = payload["deviceData"]["device_access_key"]
                db_session.add(device)
                db_session.commit()

                server.update_allowed_devices()
                payload["errors"] = []
                return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                          status=ResponseStatus.CREATED.value)
            else:
                payload["errors"] = ["Device with this ID already exists"]
                return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                          status=ResponseStatus.CONFLICT.value)
        else:
            payload["errors"] = ["No json content received"]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.NO_CONTENT.value)
    except Exception as exception:
        if payload:
            payload["errors"] = [exception.args]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.INTERNAL_SERVER_ERROR.value)
        else:
            return utils.get_response({"errors": [exception.args]}, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.BAD_REQUEST.value)


@web_service.route("/home/device.svc", methods=["PUT"])
@login_required
@roles_accepted("user", "admin")
def updateDeviceDetails():
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
    try:
        payload = None
        if request.json:
            payload = request.json
            device = DevicesList.query.get(int(payload["deviceData"]["id"]))
            device.device_id = payload["deviceData"]["device_id"]
            device.device_type = payload["deviceData"]["device_type"]
            device.device_access_key = payload["deviceData"]["device_access_key"]
            db_session.commit()

            server.update_allowed_devices()
            payload["errors"] = []
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.OK.value)
        else:
            payload["errors"] = ["No json content received"]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.NO_CONTENT.value)
    except Exception as exception:
        if payload:
            payload["errors"] = [exception.args]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.INTERNAL_SERVER_ERROR.value)
        else:
            return utils.get_response({"errors": [exception.args]}, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.BAD_REQUEST.value)


@web_service.route("/home/device.svc", methods=["DELETE"])
@login_required
@roles_accepted("user", "admin")
def deleteDevice():
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
    try:
        payload = None
        if request.json:
            payload = request.json
            device_id = payload["deviceData"]["device_id"]
            if server.get_device_by_device_id(device_id):
                DevicesList.query.filter(DevicesList.device_id == device_id).delete()
                db_session.commit()

                server.update_allowed_devices()
                payload["errors"] = []
                return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                          status=ResponseStatus.OK.value)
            else:
                payload["errors"] = ["Device with this ID doesn't exist."]
                return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                          status=ResponseStatus.NOT_FOUND.value)
        else:
            payload["errors"] = ["No json content received"]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.NO_CONTENT.value)
    except Exception as exception:
        if payload:
            payload["errors"] = [exception.args]
            return utils.get_response(payload, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.INTERNAL_SERVER_ERROR.value)
        else:
            return utils.get_response({"errors": [exception.args]}, mimetype=MimeType.JSON_MIMETYPE.value,
                                      status=ResponseStatus.BAD_REQUEST.value)
