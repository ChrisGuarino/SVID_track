import secsgem.hsms
import secsgem.common
import secsgem.gem
import code

class SimpleHost(secsgem.gem.GemHostHandler):
    def __init__(self, settings: secsgem.common.Settings):
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

code.interact("equipment object is available as variable 'h', press ctrl-d to stop", local=locals())

print("Host is running. Press Ctrl+C to stop.")
