import secsgem.hsms
import secsgem.common

class SimpleHost(secsgem.gem.GemHostHandler):
    def __init__(self, settings):
        super().__init__(settings)
        print("Host initialized")

# Define settings for the HSMS connection
settings = secsgem.hsms.HsmsSettings(
    address="127.0.0.1",
    port=5000,
    connect_mode=secsgem.hsms.HsmsConnectMode.PASSIVE,
    device_type=secsgem.common.DeviceType.HOST
)

# Create and enable the host
host = SimpleHost(settings)
host.enable()

print("Host is running. Press Ctrl+C to stop.")
