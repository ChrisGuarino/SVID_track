import secsgem.hsms
import secsgem.common

class SimpleEquipment(secsgem.gem.GemEquipmentHandler):
    def __init__(self, settings):
        super().__init__(settings)
        print("Equipment initialized")

# Define settings for the HSMS connection
settings = secsgem.hsms.HsmsSettings(
    address="127.0.0.1",
    port=5000,
    connect_mode=secsgem.hsms.HsmsConnectMode.ACTIVE,
    device_type=secsgem.common.DeviceType.EQUIPMENT
)

# Create and enable the equipment
equipment = SimpleEquipment(settings)
equipment.enable()

print("Equipment is running. Press Ctrl+C to stop.")
