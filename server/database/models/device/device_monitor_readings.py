"""
DeviceSystemMonitorReadings table model and migration/creation events container
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from server.web import db as database


class DeviceSystemMonitorReadings(database.Model):
    """
    Container for Device monitor readings
    """
    __tablename__ = "device_system_monitor_readings"
    id = Column(Integer(), primary_key=True)
    device_id = Column(Integer())
    reading_id = Column(Integer(), ForeignKey("device_system_monitor_reading_types.id"))
    reading_type = relationship("DeviceSystemMonitorReadingTypes")
    value = Column(Float())
    reported_at = Column(DateTime())
