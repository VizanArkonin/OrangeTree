"""
DeviceSystemMonitorReadings table model and migration/creation events container
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from server.database import Base


class DeviceSystemMonitorReadings(Base):
    """
    Container for Device monitor readings
    """
    __tablename__ = "device_system_monitor_readings"
    id = Column(Integer(), primary_key=True)
    device_id = Column(Integer(), ForeignKey("devices_list.id"))
    reading_id = Column(Integer())
    reading_type = relationship("DeviceSystemMonitorReadingTypes")
    value = Column(Integer())
    reported_at = Column(DateTime())
