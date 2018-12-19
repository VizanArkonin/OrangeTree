"""
Socket server - Board controller calls routing library.
"""
from datetime import datetime
from server.database import db_session
from server.socket_server import __server as server
from server.database.models.device.devices_list import DevicesList
from server.database.models.device.device_monitor_readings import DeviceSystemMonitorReadings


@server.route("DeviceStatus")
def device_status(client, data):
    """
    Processes the status and logs it into respective database tables.

    :param client: ClientThread instance
    :param data: Decrypted and deserialized packet dict
    :return: None
    """
    device_id = data["payload"]["deviceId"]

    if device_id:
        device_db_id = DevicesList.query.filter(DevicesList.device_id == device_id).first().id
        if device_db_id:
            timestamp = datetime.now()
            db_session.add(DeviceSystemMonitorReadings(device_id=device_db_id, reading_id=1,
                                                       value=data["payload"]["deviceStatus"]["cpuTemperature"],
                                                       reported_at=timestamp))
            db_session.add(DeviceSystemMonitorReadings(device_id=device_db_id, reading_id=2,
                                                       value=data["payload"]["deviceStatus"]["cpuLoadPercentage"],
                                                       reported_at=timestamp))
            db_session.add(DeviceSystemMonitorReadings(device_id=device_db_id, reading_id=3,
                                                       value=data["payload"]["deviceStatus"]["totalRam"],
                                                       reported_at=timestamp))
            db_session.add(DeviceSystemMonitorReadings(device_id=device_db_id, reading_id=4,
                                                       value=data["payload"]["deviceStatus"]["ramUsed"],
                                                       reported_at=timestamp))
            db_session.commit()
