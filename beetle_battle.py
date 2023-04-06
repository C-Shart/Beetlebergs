# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Welcome to the Ouch, Motherfucker"

# Classes
class BeetleBattle(arcade.Window):
    def __init__(self):

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Background image stored in this variable
        self.background = None

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        self.background = arcade.load_texture("Assets/Images/octagon.png")

    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

# Main code entry point
if __name__ == "__main__":
    app = BeetleBattle()
    app.setup()
    arcade.run()