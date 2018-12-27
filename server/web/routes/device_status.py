"""
Routing library for all Device status monitor related calls
"""
import json
from datetime import datetime, timedelta

from flask import render_template, request
from flask_security import login_required, roles_accepted
from sqlalchemy import and_

from server.database.models.device.device_monitor_readings import DeviceSystemMonitorReadings
from server.socket_server import server_interface
from server.web import web_service
from server.web import utils
from server.web.utils import MimeType


@web_service.route("/deviceStatus/<string:device_id>", methods=["GET"])
@login_required
@roles_accepted("admin")
def device_status(device_id):
    """
    Maps status path to respective template

    :param device_id: Device ID
    :return: Rendered template
    """
    return render_template("general/device_status.html",
                           device_id=device_id,
                           device_is_online=server_interface.is_client_alive(device_id))


@web_service.route("/deviceStatus/getMetrics/<string:device_id>", methods=["GET"])
@login_required
@roles_accepted("admin")
def get_device_status_metrics(device_id):
    """
    Request metrics data for provided device
    NOTE: Unless timespan argument is provided, route will crunch the data for the past hour.
    Timespan argument specifies the amount of past hours to include in report (i.e. 24 will equal to 1 day).

    Examples of requests:
    Without timespan                    - /deviceStatus/getMetrics/DEV_LITE
    With timespan (previous 4 hours)    - /deviceStatus/getMetrics/DEV_LITE?timespan=4

    :param device_id: Device ID
    :return: JSON details string
    """
    timespan = request.args.get("timespan", default=None)
    readings = {
        "readings": {
            "cpuTemp": [],
            "cpuLoad": [],
            "totalRam": [],
            "ramKbUsed": [],
            "ramPercentUsed": []
        }
    }
    readings_list = []

    if server_interface.is_client_alive(device_id):
        device_db_id = server_interface.get_device_db_id(device_id)
        if timespan:
            readings_list = DeviceSystemMonitorReadings. \
                query. \
                filter(
                and_(DeviceSystemMonitorReadings.reported_at >= (datetime.now() - timedelta(hours=int(timespan))),
                     DeviceSystemMonitorReadings.device_id == device_db_id)). \
                all()
        else:
            readings_list = DeviceSystemMonitorReadings. \
                query. \
                filter(
                and_(DeviceSystemMonitorReadings.reported_at >= (datetime.now() - timedelta(hours=1)),
                     DeviceSystemMonitorReadings.device_id == device_db_id)). \
                all()

    for reading in readings_list:
        if reading.reading_id == 1:
            readings["readings"]["cpuTemp"].append(reading.get_value_timestamp_dict())
        elif reading.reading_id == 2:
            readings["readings"]["cpuLoad"].append(reading.get_value_timestamp_dict())
        elif reading.reading_id == 3:
            readings["readings"]["totalRam"].append(reading.get_value_timestamp_dict())
        elif reading.reading_id == 4:
            readings["readings"]["ramKbUsed"].append(reading.get_value_timestamp_dict())
        elif reading.reading_id == 5:
            readings["readings"]["ramKbUsed"].append(reading.get_value_timestamp_dict())

    return utils.get_response(json.dumps(readings), mimetype=MimeType.JSON_MIMETYPE.value)
