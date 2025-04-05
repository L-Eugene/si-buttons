from playsound import playsound
from player import Player

class GameController:
    def __init__(self, game_ui, device_manager, players, game_master):
        """
        Initializes the GameController.

        :param game_ui: The GameUI instance.
        :param device_manager: The DeviceManager instance.
        :param players: A list of Player instances.
        :param game_master: The game master Player instance.
        """
        self.game_ui = game_ui
        self.device_manager = device_manager
        self.players = players
        self.game_master = game_master
        self.config_state = 0
        self.update_ui_for_config_state()

    def handle_esc_pressed(self):
        """
        Handles the Esc key press event.
        """
        print("Esc pressed")
        if isinstance(self.config_state, int) and self.config_state < len(self.players):
            # Skip current player during configuration
            self.config_state += 1
            self.update_ui_for_config_state()
        elif isinstance(self.config_state, int) and self.config_state == len(self.players):
            # Skip game master during configuration
            self.config_state = 'game'
            self.update_ui_for_config_state()
        elif any(player.status == "answer" for player in self.players):
            # Reset answer state during the game
            for player in self.players:
                player.status = None
            self.config_state = 'game'
            self.update_ui_for_config_state()

    def handle_left_click(self, device):
        """
        Handles a left mouse click event.
        """
        print(f"Left click on device: {device.name}")
        if isinstance(self.config_state, int) and device.path not in self.assigned_devices():
            if self.config_state < len(self.players):
                self.players[self.config_state].assign_device(device.path)
                self.config_state += 1
                self.update_ui_for_config_state()
            elif self.config_state == len(self.players):
                self.game_master.assign_device(device.path)
                self.config_state = 'game'
                self.update_ui_for_config_state()
        elif not isinstance(self.config_state, int) and all(player.status != "answer" for player in self.players):
            player = next((p for p in self.players if p.device == device.path), None)
            if player:
                self.config_state = player
                self.update_ui_for_config_state()
        elif any(player.status == "answer" for player in self.players) and device.path == self.game_master.device:
            for player in self.players:
                player.status = None
            self.config_state = 'game'
            self.update_ui_for_config_state()

    def update_ui_for_config_state(self):
        """
        Updates the UI based on the current configuration state.
        """
        if isinstance(self.config_state, int) and self.config_state < len(self.players):
            self.game_ui.update_device_label(f"Выберите устройство для игрока {self.config_state + 1}")
            for i, player in enumerate(self.players):
                player.status = "config" if i == self.config_state else None
        elif isinstance(self.config_state, int):
            self.game_ui.update_device_label("Выберите устройство для ведущего")
            for player in self.players:
                player.status = None
        elif isinstance(self.config_state, Player):
            self.game_ui.update_device_label(f"Отвечает {self.config_state.name}")
            playsound("sound.mp3", block=False)
            self.config_state.status = "answer"
        else:
            self.game_ui.update_device_label("Игра идет")

    def assigned_devices(self):
        """
        Returns a list of all assigned devices.
        """
        return [player.device for player in self.players if player.device] + ([self.game_master.device] if self.game_master.device else [])