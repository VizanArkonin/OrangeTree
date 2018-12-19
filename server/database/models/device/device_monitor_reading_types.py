"""
DeviceSystemMonitorReadingTypes table model and migration/creation events container
"""
from sqlalchemy import Column, Integer, String, ForeignKey, event

from server.database import Base, db_session


class DeviceSystemMonitorReadingTypes(Base):
    """
    Defines the reading types for device system monitor readings
    """
    __tablename__ = "device_system_monitor_reading_types"
    id = Column(Integer(), ForeignKey("device_system_monitor_readings.reading_id"), primary_key=True)
    reading_type_name = Column(String(40))


"""
Initiation/migrations section.
TODO: Rework initiation functions to use static data (i.e. JSON data providers)
"""


@event.listens_for(DeviceSystemMonitorReadingTypes.__table__, "after_create")
def populate_default_reading_types(*args, **kwargs):
    db_session.add(DeviceSystemMonitorReadingTypes(id=1, reading_type_name="CPU Temperature, °C"))
    db_session.add(DeviceSystemMonitorReadingTypes(id=2, reading_type_name="CPU Load, %"))
    db_session.add(DeviceSystemMonitorReadingTypes(id=3, reading_type_name="Total RAM, kB"))
    db_session.add(DeviceSystemMonitorReadingTypes(id=4, reading_type_name="Ram used, kB"))
    db_session.commit()
