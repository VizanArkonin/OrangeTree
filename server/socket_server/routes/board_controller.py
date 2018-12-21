"""
Socket server - Board controller calls routing library.
"""
from datetime import datetime
from server.web import db as database
from server.socket_server import __server as server
from server.database.models.device.devices import Devices
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
        device_db_id = Devices.query.filter(Devices.device_id == device_id).first().id
        if device_db_id:
            timestamp = datetime.now()
            database.session.add(DeviceSystemMonitorReadings(device_id=device_db_id, reading_id=1,
                                                             value=data["payload"]["deviceStatus"]["cpuTemperature"],
                                                             reported_at=timestamp))
            database.session.add(DeviceSystemMonitorReadings(device_id=device_db_id, reading_id=2,
                                                             value=data["payload"]["deviceStatus"]["cpuLoadPercentage"],
                                                             reported_at=timestamp))
            database.session.add(DeviceSystemMonitorReadings(device_id=device_db_id, reading_id=3,
                                                             value=data["payload"]["deviceStatus"]["totalRam"],
                                                             reported_at=timestamp))
            database.session.add(DeviceSystemMonitorReadings(device_id=device_db_id, reading_id=4,
                                                             value=data["payload"]["deviceStatus"]["ramUsed"],
                                                             reported_at=timestamp))
            database.session.commit()
