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


class DeviceTypes(Base):
    """
    Defines the device types
    """
    __tablename__ = 'device_types'
    type_id = Column(Integer(), primary_key=True)
    type_name = Column(String(40))
