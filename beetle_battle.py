# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Welcome to Arcade"
RADIUS = 150

# Classes
class BeetleBattle(arcade.Window):
    def __init__(self):

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        # Clear the screen and start drawing
        arcade.start_render()

        # Draw a blue circle
        arcade.draw_circle_filled(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, RADIUS, arcade.color.BLUE
        )

# Main code entry point
if __name__ == "__main__":
    app = BeetleBattle()
    arcade.run()