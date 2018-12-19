from sqlalchemy import Column, Integer, String, DateTime, event
from sqlalchemy.orm import relationship
from client.config import CLIENT_CONFIG

from server.database import Base, db_session
from common.general import get_time_formatter


class DevicesList(Base):
    """
    Table that contains allowed devices
    """
    __tablename__ = 'devices_list'
    id = Column(Integer(), primary_key=True)
    device_id = Column(String(40), unique=True)
    device_type_id = Column(Integer())
    device_access_key = Column(String(80))
    last_address = Column(String(40))
    last_connected_at = Column(DateTime())

    device_type = relationship("DeviceTypes", backref="devices_list")
    device_config = relationship("DeviceTypePinConfig", backref="devices_list")

    device_system_readings = relationship("DeviceSystemMonitorReadings", backref="devices_list")

    def serialize_general_data(self):
        """
        Serializes non-sensual information about the device (i.e. excluding access key)
        :return: Dict with data
        """
        return {
            "id": self.id,
            "device_id": self.device_id,
            "device_type": self.device_type_id,
            "last_address": self.last_address,
            "last_connected_at": self.last_connected_at.strftime(get_time_formatter())
            }

    def serialize_all(self):
        """
        Serializes all variables, providing full information about device.
        :return: Dict with data
        """
        return {
            "id": self.id,
            "device_id": self.device_id,
            "device_type": self.device_type_id,
            "device_access_key": self.device_access_key
            }

    def serialize_config(self):
        """
        Serializes config.
        :return: Dict with config data
        """
        config_list = []
        for row in self.device_config:
            config_row = {
                "number": row.pin_number,
                "wPi": row.pin_wpi,
                "type": row.pin_type[0].type_name,
                "meta": row.pin_meta
            }
            config_list.append(config_row)

        return {"pins": config_list}


"""
Initiation/migrations section.
TODO: Rework initiation functions to use static data (i.e. JSON data providers)
"""


@event.listens_for(DevicesList.__table__, "after_create")
def populate_default_device_types(*args, **kwargs):
    db_session.add(DevicesList(device_id=CLIENT_CONFIG["device_id"], device_type_id=CLIENT_CONFIG["device_type"],
                               device_access_key=CLIENT_CONFIG["device_key"]))
    db_session.commit()
