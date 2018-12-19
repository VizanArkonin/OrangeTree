"""
DeviceTypes table model and migration/creation events container
"""
from sqlalchemy import Column, Integer, String, ForeignKey, event
from server.database import Base, db_session


class DeviceTypes(Base):
    """
    Defines the device types
    """
    __tablename__ = 'device_types'
    device_type_id = Column(Integer(), ForeignKey("devices_list.device_type_id"), primary_key=True)
    type_name = Column(String(40))


"""
Initiation/migrations section.
TODO: Rework initiation functions to use static data (i.e. JSON data providers)
"""


@event.listens_for(DeviceTypes.__table__, "after_create")
def populate_default_device_types(*args, **kwargs):
    db_session.add(DeviceTypes(device_type_id=1, type_name="Orange PI Lite (Wi-Fi)"))
    db_session.commit()
