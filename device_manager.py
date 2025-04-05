from evdev import InputDevice, ecodes, list_devices
import threading

class DeviceManager:
    def __init__(self):
        """
        Initializes the DeviceManager and starts monitoring input devices.
        """
        self.devices = []
        self.event_handlers = []
        self.monitoring_threads = []

        # Detect devices during initialization
        self.detect_devices()

    def detect_devices(self):
        """
        Detects all input devices that support relative motion (e.g., mouse) or key events.
        """
        self.devices = [
            dev
            for dev in [InputDevice(path) for path in list_devices()]
            # EV_REL for relative motion (e.g., mouse) or EV_KEY for key events (e.g., keyboard)
            if ecodes.EV_REL in dev.capabilities() or ecodes.EV_KEY in dev.capabilities()
        ]

    def register_event_handler(self, handler):
        """
        Registers an event handler to be notified of input events.

        :param handler: A callable that takes two arguments: device and event.
        """
        self.event_handlers.append(handler)

    def start_monitoring(self):
        """
        Starts monitoring all detected devices for input events.
        """
        for device in self.devices:
            thread = threading.Thread(target=self._monitor_device, args=(device,), daemon=True)
            thread.start()
            self.monitoring_threads.append(thread)

    def _monitor_device(self, device):
        """
        Monitors a single device for input events and notifies registered handlers.

        :param device: The InputDevice to monitor.
        """
        for event in device.read_loop():
            # Filter relevant events
            if event.type == ecodes.EV_KEY and event.value == 1:
                for handler in self.event_handlers:
                    handler(device, event)