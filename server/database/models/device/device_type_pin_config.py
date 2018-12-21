"""
DeviceTypePinConfig table model and migration/creation events container
"""
from sqlalchemy import Column, Integer, String, ForeignKey, event
from sqlalchemy.orm import relationship

from server.web import db as database


class DeviceTypePinConfig(database.Model):
    """
    Container for GPIO Pin configurations for each device type.
    """
    __tablename__ = "device_type_pin_config"
    id = Column(Integer(), primary_key=True)
    device_type_id = Column(Integer(), ForeignKey("device_types.device_type_id"))
    pin_number = Column(Integer())
    pin_wpi = Column(Integer())
    pin_type_id = Column(Integer(), ForeignKey("device_pin_types.pin_type_id"))
    pin_type = relationship("DevicePinTypes")
    pin_meta = Column(String(40))


"""
Initiation/migrations section.
TODO: Rework initiation functions to use static data (i.e. JSON data providers)
"""


@event.listens_for(DeviceTypePinConfig.__table__, "after_create")
def populate_orangepi_lite_wifi_pins(*args, **kwargs):
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=1, pin_type_id=3))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=2, pin_type_id=4))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=3, pin_wpi=8, pin_type_id=1,
                                             pin_meta="PA12/TWI0/SDA/DI_RX"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=4, pin_type_id=4))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=5, pin_wpi=9, pin_type_id=1,
                                             pin_meta="PA11/TWI0_SCK/DI_TX/SLC"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=6, pin_type_id=2))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=7, pin_wpi=7, pin_type_id=1,
                                             pin_meta="PA6/SIM_PWREN/PWM1"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=8, pin_wpi=15, pin_type_id=1,
                                             pin_meta="PA13/SPI1_CS/UART3_TX"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=9, pin_type_id=2))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=10, pin_wpi=16, pin_type_id=1,
                                             pin_meta="PA14/SPI1_CLK/UART_RX"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=11, pin_wpi=0, pin_type_id=1,
                                             pin_meta="PA1/UART2_RX/JTAG_CK"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=12, pin_wpi=1, pin_type_id=1,
                                             pin_meta="PD14/RGMII_NULL"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=13, pin_wpi=2, pin_type_id=1,
                                             pin_meta="PA0/UART2_TX/JTAG_MS"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=14, pin_type_id=2))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=15, pin_wpi=3, pin_type_id=1,
                                             pin_meta="PA3/UART2_CTS/JTAG_DI"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=16, pin_wpi=4, pin_type_id=1,
                                             pin_meta="PC4/NCE0"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=17, pin_type_id=3))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=18, pin_wpi=5, pin_type_id=1,
                                             pin_meta="PC7/NRB1"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=19, pin_wpi=12, pin_type_id=1,
                                             pin_meta="PC0/NAND_WE#/SPI0_MOSI"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=20, pin_type_id=2))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=21, pin_wpi=13, pin_type_id=1,
                                             pin_meta="PC1/NALE/SPI0_MISO"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=22, pin_wpi=6, pin_type_id=1,
                                             pin_meta="PA2/UART2_RTS/JTAG_DO"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=23, pin_wpi=14, pin_type_id=1,
                                             pin_meta="PC2/NCLE/SPI0_CLK"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=24, pin_wpi=10, pin_type_id=1,
                                             pin_meta="PC3/NCE1/SPI0_CS"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=25, pin_type_id=2))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=26, pin_wpi=11, pin_type_id=1,
                                             pin_meta="PA21/PCM0_DIN/SIM_VPPEN"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=27, pin_wpi=30, pin_type_id=1,
                                             pin_meta="PA19/PCM0_CLK/TWI1_SDA"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=28, pin_wpi=31, pin_type_id=1,
                                             pin_meta="PA18/PCM0_SYNC/TWI1_SCK"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=29, pin_wpi=21, pin_type_id=1,
                                             pin_meta="PA7/SIM_CLK"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=30, pin_type_id=2))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=31, pin_wpi=22, pin_type_id=1,
                                             pin_meta="PA8/SIM_DATA"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=32, pin_wpi=26, pin_type_id=1,
                                             pin_meta="PG8/UART1_RTS"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=33, pin_wpi=23, pin_type_id=1,
                                             pin_meta="PA9/SIM_RST"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=34, pin_type_id=2))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=35, pin_wpi=24, pin_type_id=1,
                                             pin_meta="PA10/SIM_DET"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=36, pin_wpi=27, pin_type_id=1,
                                             pin_meta="PG9/UART1_CTS"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=37, pin_wpi=25, pin_type_id=1,
                                             pin_meta="PA20/PCM0_DOUT/SIM_VPPEN"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=38, pin_wpi=28, pin_type_id=1,
                                             pin_meta="PG6/UART1_TX"))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=39, pin_type_id=2))
    database.session.add(DeviceTypePinConfig(device_type_id=1, pin_number=40, pin_wpi=29, pin_type_id=1,
                                             pin_meta="PG7/UART1_RX"))
    database.session.commit()
