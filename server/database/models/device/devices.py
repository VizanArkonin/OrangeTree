from sqlalchemy import Column, Integer, String, DateTime, event, ForeignKey
from sqlalchemy.orm import relationship
from client.config import CLIENT_CONFIG

from common.general import get_time_formatter
from server.web import db as database


class Devices(database.Model):
    """
    Table that contains allowed devices
    """
    __tablename__ = 'devices'
    id = Column(Integer(), primary_key=True)
    device_id = Column(String(40), unique=True)
    device_type_id = Column(Integer(), ForeignKey("device_types.device_type_id"))
    device_access_key = Column(String(80))
    last_address = Column(String(40))
    last_connected_at = Column(DateTime())

    device_type = relationship("DeviceTypes", backref="devices")

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
                                 if self.last_connected_at
                                 else None
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
        for row in self.device_type.device_config:
            config_row = {
                "number": row.pin_number,
                "wPi": row.pin_wpi,
                "type": row.pin_type.type_name,
                "meta": row.pin_meta
            }
            config_list.append(config_row)

        return {"pins": config_list}


"""
Initiation/migrations section.
TODO: Rework initiation functions to use static data (i.e. JSON data providers)
"""


@event.listens_for(Devices.__table__, "after_create")
def populate_default_device_types(*args, **kwargs):
    database.session.add(Devices(device_id=CLIENT_CONFIG["device_id"], device_type_id=CLIENT_CONFIG["device_type"],
                                 device_access_key=CLIENT_CONFIG["device_key"]))
    database.session.commit()
