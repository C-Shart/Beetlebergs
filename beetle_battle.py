# Basic arcade program using objects
# Displays a white window with a blue circle in the middle

# Imports
import arcade

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Welcome to Arcade"

# Scaling constants
BEETLE_SCALING = .65

# Classes
class BeetleBattle(arcade.Window):
    def __init__(self):

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Beetle sprites in this variable
        self.beetle_list = None
        self.beetle_sprite = None

        # Background image stored in this variable
        self.background = None

        # Set the background window
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        # Create the background
        self.background = arcade.load_texture("Assets/Images/octagon.png")

        # Create sprite lists
        self.beetle_list = arcade.SpriteList()

        # Set up the beetle and place it at these coordinates
        beetle_sprite_source = "Assets/Sprites/beetle_GRN.png"
        self.beetle_sprite = arcade.Sprite(beetle_sprite_source, BEETLE_SCALING)
        self.beetle_sprite.center_x = 70
        self.beetle_sprite.center_y = 65
        self.beetle_list.append(self.beetle_sprite)

    def on_draw(self):
        # Clear the screen
        arcade.start_render()

        # Start drawing
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.beetle_list.draw()



# Main code entry point
if __name__ == "__main__":
    app = BeetleBattle()
    app.setup()
    arcade.run()