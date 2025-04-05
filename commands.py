class Command:
    """
    Base class for all commands.
    """
    def execute(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the execute method.")


class EscPressedCommand(Command):
    """
    Command to handle the Esc key press.
    """
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def execute(self, *args, **kwargs):
        self.game_controller.handle_esc_pressed()


class LeftClickCommand(Command):
    """
    Command to handle a left mouse click.
    """
    def __init__(self, game_controller):
        self.game_controller = game_controller

    def execute(self, device, *args, **kwargs):
        self.game_controller.handle_left_click(device)