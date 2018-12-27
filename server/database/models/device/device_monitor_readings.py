"""
DeviceSystemMonitorReadings table model and migration/creation events container
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from server.web import db as database
from common.general import get_time_formatter


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

    def serialize(self):
        """
        Serializes the data into dict.
        :return: Dict with data.
        """
        return {
            "device_id": self.device_id,
            "reading_id": self.reading_id,
            "reading_type": self.reading_type.reading_type_name,
            "value": self.value,
            "reported_at": self.reported_at.strftime(get_time_formatter())
        }

    def get_value_timestamp_dict(self):
        """
        Returns a value-timestamp pair dict, used in data array composing.
        :return: Dict with value and timestamp.
        """
        return {
            "value": self.value,
            "timestamp": self.reported_at.strftime(get_time_formatter())
        }
