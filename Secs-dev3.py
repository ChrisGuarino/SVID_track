import logging
import secsgem.common
import secsgem.gem
import secsgem.hsms
import secsgem.secs
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import code  # Added import

from communication_log_file_handler import CommunicationLogFileHandler

class LoggingEquipmentHandler(secsgem.gem.GemEquipmentHandler):
    def __init__(self, settings: secsgem.common.Settings):
        super().__init__(settings)
        self.MDLN = "logging_equipment"
        self.SOFTREV = "1.0.0"
        self.sv1 = 2043
        self.sv2 = "example_status_variable"
        self.data = []  # List to store captured data

        self.status_variables.update({
            10: secsgem.gem.StatusVariable(10, "Numeric SVID, U4", "units", secsgem.secs.variables.U4),
            "SV2": secsgem.gem.StatusVariable("SV2", "Text SVID, String", "chars", secsgem.secs.variables.String),
        })

    def on_sv_value_request(self, svid, sv):
        logging.info(f"Received Status Variable Request: SVID={svid}")
        if svid == 2043:
            value = sv.value_type(self.sv1)
            logging.info(f"Captured Value for SVID 10: {value}")
            self.data.append(value)  # Capture data
        elif svid == "SV2":
            value = sv.value_type(self.sv2)
            logging.info(f"Captured Value for SVID SV2: {value}")
            self.data.append(value)
        return sv.value_type(self.sv1)

# Configure logging
commLogFileHandler = CommunicationLogFileHandler("machine_data.log", "a")
commLogFileHandler.setFormatter(logging.Formatter("%(asctime)s: %(message)s"))
logging.getLogger("communication").addHandler(commLogFileHandler)
logging.getLogger("communication").propagate = False

logging.basicConfig(format='%(asctime)s %(name)s.%(funcName)s: %(message)s', level=logging.INFO)

settings = secsgem.hsms.HsmsSettings(
    address="127.0.0.1",  # Replace with your machine's IP address
    port=5000,            # Replace with the correct port number
    connect_mode=secsgem.hsms.HsmsConnectMode.ACTIVE,
    device_type=secsgem.common.DeviceType.EQUIPMENT
)

handler = LoggingEquipmentHandler(settings)
handler.enable()



code.interact("Equipment object is available as variable 'handler'", local=locals())

# Plotting Setup
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot(x_data, y_data, '-')

def update_plot(frame):
    if handler.data:
        x_data.append(len(x_data))  # X-axis is the time step
        y_data.append(handler.data[-1])  # Y-axis is the latest data point
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()
    return line,

ani = animation.FuncAnimation(fig, update_plot, blit=True, interval=1000, cache_frame_data=False)

plt.xlabel('Time Step')
plt.ylabel('Value')
plt.title('Live Data Plot')
plt.grid(True)
plt.show()


