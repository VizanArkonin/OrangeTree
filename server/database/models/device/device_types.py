"""
DeviceTypes table model and migration/creation events container
"""
from sqlalchemy import Column, Integer, String, event
from sqlalchemy.orm import relationship

from server.web import db as database


class DeviceTypes(database.Model):
    """
    Defines the device types
    """
    __tablename__ = 'device_types'
    device_type_id = Column(Integer(), primary_key=True)
    type_name = Column(String(40))
    device_config = relationship("DeviceTypePinConfig", backref="device_types")


"""
Initiation/migrations section.
TODO: Rework initiation functions to use static data (i.e. JSON data providers)
"""


@event.listens_for(DeviceTypes.__table__, "after_create")
def populate_default_device_types(*args, **kwargs):
    database.session.add(DeviceTypes(device_type_id=1, type_name="Orange PI Lite (Wi-Fi)"))
    database.session.commit()
