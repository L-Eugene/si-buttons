class Player:
    def __init__(self, name, color, ui_square):
        """
        Initializes a Player instance.

        :param name: The name of the player.
        :param color: The color associated with the player.
        :param ui_square: The UI square (Canvas) representing the player in the GameUI.
        """
        self.name = name
        self.color = color
        self.ui_square = ui_square
        self.device = None
        self._status = None

    @property
    def status(self):
        """
        Gets the current status of the player.
        """
        return self._status

    @status.setter
    def status(self, value):
        """
        Sets the status of the player and updates the UI square accordingly.

        :param value: The new status of the player (e.g., "config", "answer", or None).
        """
        self._status = value
        if value == "config":
            self.ui_square.config(highlightbackground="blue")
        elif value == "answer":
            self.ui_square.config(highlightbackground="green")
        else:
            self.ui_square.config(highlightbackground=self.color)

    def assign_device(self, device):
        """
        Assigns an input device to the player.

        :param device: The input device to assign to the player.
        """
        self.device = device

    def reset(self):
        """
        Resets the player's state and UI square to the default state.
        """
        self.device = None
        self.status = None