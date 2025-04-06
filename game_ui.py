import tkinter as tk

class GameUI:
    def __init__(self, root, num_players=4, colors=["red", "yellow", "violet", "orange"]):
        """
        Initializes the GameUI with the given root window and number of players.

        :param root: The tkinter root window.
        :param num_players: The number of player squares to create.
        :param colors: A list of colors for the player squares.
        """
        self.root = root
        self.root.title("Mouse Clicker Game")

        self.num_players = num_players

        # Create player squares
        self.player_squares = []
        for i in range(num_players):
            square = tk.Canvas(root, width=100, height=100, bg=colors[i], highlightthickness=4)
            square.grid(row=0, column=i, padx=5, pady=5)
            self.player_squares.append(square)

        # Create device label
        self.device_label = tk.Label(root, text="Device: None", font=("Arial", 14))
        self.device_label.grid(row=1, columnspan=self.num_players, pady=10)
        self.fix_mouse_position()

    def fix_mouse_position(self):
        self.root.event_generate('<Motion>', warp=True, x=230, y=20)

    def update_device_label(self, text):
        """
        Updates the device label with the given text.

        :param text: The text to display in the device label.
        """
        self.device_label.config(text=text)
