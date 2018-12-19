"""
DevicePinTypes table model and migration/creation events container
"""
from sqlalchemy import Column, Integer, String, ForeignKey, event
from server.database import Base, db_session


class DevicePinTypes(Base):
    """
    Defines the pin types
    """
    __tablename__ = "device_pin_types"
    pin_type_id = Column(Integer(), ForeignKey("device_type_pin_config.pin_type_id"), primary_key=True)
    type_name = Column(String(40))


"""
Initiation/migrations section.
TODO: Rework initiation functions to use static data (i.e. JSON data providers)
"""


@event.listens_for(DevicePinTypes.__table__, "after_create")
def populate_default_pin_types(*args, **kwargs):
    db_session.add(DevicePinTypes(pin_type_id=1, type_name="wPi"))
    db_session.add(DevicePinTypes(pin_type_id=2, type_name="ground"))
    db_session.add(DevicePinTypes(pin_type_id=3, type_name="3.3_power"))
    db_session.add(DevicePinTypes(pin_type_id=4, type_name="5_power"))
    db_session.commit()
