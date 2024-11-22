import logging
import secsgem.common
import secsgem.gem
import secsgem.hsms
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import code  # For interactive debugging

# Logging Setup
logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.INFO)

# Custom Communication Logger
class CommunicationLogFileHandler(logging.Handler):
    """Custom logging handler to write logs to a file."""
    def __init__(self, path):
        super().__init__()
        self.path = path

    def emit(self, record):
        with open(self.path, 'a') as f:
            f.write(self.format(record) + "\n")

# Equipment Handler Class
class SimpleEquipmentHandler(secsgem.gem.GemEquipmentHandler):
    """Handles equipment communication and responds to requests."""
    def __init__(self, settings):
        super().__init__(settings)
        self.data = []  # Captured data
        self.sv_value = 2043  # Example status variable value
        
        # Define Status Variables
        self.status_variables.update({
            10: secsgem.gem.StatusVariable(10, "Numeric Variable", "units", secsgem.secs.variables.U4),
        })

    def on_sv_value_request(self, svid, sv):
        """Handle requests for status variable values."""
        logging.info(f"Request received for SVID={svid}")
        if svid == 10:  # If SVID matches
            value = sv.value_type(self.sv_value)  # Example value for SVID 10
            self.data.append(value)  # Log data
            logging.info(f"Value captured: {value}")
            return value
        return None

# HSMS Settings
settings = secsgem.hsms.HsmsSettings(
    address="127.0.0.1",  # Localhost for testing
    port=5000,  # Port for communication
    connect_mode=secsgem.hsms.HsmsConnectMode.ACTIVE,  # Active mode
    device_type=secsgem.common.DeviceType.EQUIPMENT  # Equipment type
)

# Initialize Equipment Handler
handler = SimpleEquipmentHandler(settings)
handler.enable()

# Interactive Shell for Testing
code.interact("Handler is available as 'handler'", local=locals())

# Plotting Live Data
fig, ax = plt.subplots()
x_data, y_data = [], []
line, = ax.plot(x_data, y_data, '-')

def update_plot(frame):
    """Update the live plot with new data."""
    if handler.data:
        x_data.append(len(x_data))  # Use the index as the x-axis
        y_data.append(handler.data[-1])  # Latest value for y-axis
        line.set_data(x_data, y_data)
        ax.relim()
        ax.autoscale_view()
    return line,

# Save after sufficient data is added
def save_plot():
    plt.savefig('plot.png')
    print("Plot saved as 'plot.png'")

# Call this function after generating enough data
save_plot()

# Animate the Plot
#ani = animation.FuncAnimation(fig, update_plot, blit=True, interval=1000)

# Show the Plot
# plt.xlabel('Time Step')
# plt.ylabel('Value')
# plt.title('Live Data Plot')
# plt.grid(True)
# plt.show()

x_data = list(range(10))  # Simulate 10 time steps
y_data = [i * 2 for i in x_data]  # Simulate some Y-axis data

plt.plot(x_data, y_data, '-')
plt.xlabel('Time Step')
plt.ylabel('Value')
plt.title('Test Plot')
plt.grid(True)
plt.savefig('plot.png')
plt.show()