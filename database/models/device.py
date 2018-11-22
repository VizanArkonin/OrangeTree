from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database import Base
from utils.general import get_time_formatter


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


class DeviceTypes(Base):
    """
    Defines the device types
    """
    __tablename__ = 'device_types'
    device_type_id = Column(Integer(), ForeignKey("devices_list.device_type_id"), primary_key=True)
    type_name = Column(String(40))


class DevicePinTypes(Base):
    """
    Defines the pin types
    """
    __tablename__ = "device_pin_types"
    pin_type_id = Column(Integer(), ForeignKey("device_type_pin_config.pin_type_id"), primary_key=True)
    type_name = Column(String(40))


class DeviceTypePinConfig(Base):
    """
    Container for GPIO Pin configurations for each device type.
    """
    __tablename__ = "device_type_pin_config"
    id = Column(Integer(), primary_key=True)
    device_type_id = Column(Integer(), ForeignKey("devices_list.device_type_id"))
    pin_number = Column(Integer())
    pin_wpi = Column(Integer())
    pin_type_id = Column(Integer())
    pin_type = relationship("DevicePinTypes")
    pin_meta = Column(String(40))
