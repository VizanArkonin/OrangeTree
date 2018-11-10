from sqlalchemy import Column, Integer, String

from database import Base


class DevicesList(Base):
    """
    Table that contains allowed devices
    """
    __tablename__ = 'devices_list'
    id = Column(Integer(), primary_key=True)
    device_id = Column(String(40), unique=True)
    device_type = Column(Integer())
    device_access_key = Column(String(80))

    def serialize_general_data(self):
        """
        Serializes non-sensual information about the device (i.e. excluding access key)
        :return: Dict with data
        """
        return {
            "id": self.id,
            "device_id": self.device_id,
            "device_type": self.device_type
            }

    def serialize_all(self):
        """
        Serializes all variables, providing full information about device.
        :return: Dict with data
        """
        return {
            "id": self.id,
            "device_id": self.device_id,
            "device_type": self.device_type,
            "device_access_key": self.device_access_key
            }


class DeviceTypes(Base):
    """
    Defines the device types
    """
    __tablename__ = 'device_types'
    type_id = Column(Integer(), primary_key=True)
    type_name = Column(String(40))
