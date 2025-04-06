from commands import EscPressedCommand, LeftClickCommand
from game_controller import GameController
from device_manager import DeviceManager
from game_ui import GameUI
from player import Player
import tkinter as tk
from evdev import ecodes

# Initialize components
root = tk.Tk()
game_ui = GameUI(root, num_players=3)
device_manager = DeviceManager()
players = [Player(f"игрок {i+1}", game_ui.player_squares[i]) for i in range(len(game_ui.player_squares))]
game_master = Player("Ведущий", None)
game_controller = GameController(game_ui, device_manager, players, game_master)

# Register commands
esc_command = EscPressedCommand(game_controller)
left_click_command = LeftClickCommand(game_controller)

device_manager.register_event_handler(lambda device, event: esc_command.execute() if event.code == ecodes.KEY_ESC else None)
device_manager.register_event_handler(lambda device, event: left_click_command.execute(device) if event.code == ecodes.BTN_LEFT else None)

def mouse_center_loop():
    game_ui.fix_mouse_position()
    root.after(50, mouse_center_loop)
root.after(100, mouse_center_loop)

# Start the application
device_manager.start_monitoring()
root.mainloop()