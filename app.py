import tkinter as tk
from evdev import InputDevice, ecodes, list_devices
from playsound import playsound
import threading

class Actor:
    def __init__(self, name, window = None, color = None):
        if color is None:
            self.square = None
        else:
            self.square = tk.Canvas(window, width=100, height=100, bg=color, highlightthickness=4)

        self.name = name
        self._status = None
        self.device = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        if value == "config":
            self.square.config(highlightbackground="blue")
        elif value == "answer":
            self.square.config(highlightbackground="green")
            playsound("sound.mp3", block=False)
        else:
            self.square.config(highlightbackground=self.square["bg"])

    def __str__(self):
        return f"Actor(name={self.name}, device={self.device})"

class MouseClickAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse SI")

        self.config_state = None

        self.players = [None] * 4
        self.game_master = Actor("Ведущий")

        colors = ["red", "yellow", "violet", "orange"]
        for i, color in enumerate(colors):
            self.players[i] = Actor(f"игрок {i + 1}", self.root, color)
            self.players[i].square.grid(row=0, column=i, padx=5, pady=5)

        self.device_label = tk.Label(root, text="Device: None", font=("Arial", 14))
        self.device_label.grid(row=1, columnspan=4, pady=10)

        self.device_thread = threading.Thread(target=self.monitor_devices, daemon=True)
        self.device_thread.start()

        self.set_config_state(0)
        self.center_mouse()

    @property
    def assigned_devices(self):
        assigned = []
        for player in self.players:
            if player.device is not None:
                assigned.append(player.device)
        if self.game_master.device is not None:
            assigned.append(self.game_master.device)

        return assigned

    def center_mouse(self):
        self.root.event_generate('<Motion>', warp=True, x=230, y=20)

    def set_config_state(self, state):
        self.config_state = state

        if isinstance(state, int) and state < len(self.players):
            self.device_label.config(text=f"Выберите мышку для игрока №{state+1}")
            for i, player in enumerate(self.players):
                if i == state:
                    player.status = "config"
                else:
                    player.status = None
        elif isinstance(state, int):
            self.device_label.config(text=f"Выберите мышку для ведущего")
            for player in self.players:
                player.status = None
        elif isinstance(state, Actor):
            self.device_label.config(text=f"Отвечает {state.name}")
            state.status = "answer"
        else:
            self.device_label.config(text=f"ИГРА")

    def monitor_devices(self):
        devices = [
            dev 
            for dev in [InputDevice(path) for path in list_devices()]
            if ecodes.EV_REL in dev.capabilities() or ecodes.EV_KEY in dev.capabilities()
        ]

        for dev in devices:
            threading.Thread(target=self.read_device_events, args=(dev,), daemon=True).start()

    def read_device_events(self, device):
        for event in device.read_loop():
            self.center_mouse()
            if event.type == ecodes.EV_KEY and event.value == 1:  # Button press
                if event.code == ecodes.KEY_ESC:
                    if isinstance(self.config_state, int) and self.config_state < len(self.players):
                        # If Esc is pressed during configuration - skip current player
                        self.set_config_state(self.config_state + 1)
                    elif isinstance(self.config_state, int) and self.config_state == len(self.players):
                        # If Esc is pressed during configuration - skip game master
                        self.set_config_state('game')
                    elif any([p.status == "answer" for p in self.players]):
                        # If Esc is pressed during game - reset the answer status
                        for player in self.players:
                            player.status = None
                        self.set_config_state('game')
                if event.code == ecodes.BTN_LEFT:
                    # If the code is a number - we're in config mode
                    # Value less than self.squares size mean we're choosing the mouse for player,
                    # Value equal to self.squares size mean we are selecting the mouse for game master
                    if isinstance(self.config_state, int) and not device.path in self.assigned_devices:
                        # TODO: check if current device already assigned to someone
                        if self.config_state < len(self.players):
                            self.players[self.config_state].device = device.path
                            self.set_config_state(self.config_state + 1)
                        elif self.config_state == len(self.players):
                            self.game_master.device = device.path
                            self.set_config_state('game')
                        else:
                            self.set_config_state('game')
                        print(f"Current config state is: {self.config_state}")
                    elif not isinstance(self.config_state, int) and all([p.status != "answer" for p in self.players]):
                        player = next((p for p in self.players if p.device == device.path), None)
                        if player:
                            self.set_config_state(player)
                    elif any([p.status == "answer" for p in self.players]) and device.path == self.game_master.device:
                        # If the game master mouse is pressed and any player is in answer state
                        for player in self.players:
                            player.status = None
                        self.set_config_state('game')

                    print(f"Button {event.code} pressed on {device.name} ({device.path})")

    def on_close(self):
        self.device_thread.join()  # Wait for the device monitoring thread to finish
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseClickAnalyzer(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()