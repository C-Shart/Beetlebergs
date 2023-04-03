import arcade

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Welcome to Arcade"

BEETLE_SPRITE_PATH_GREEN = "Assets/Sprites/beetle_GRN.png"
BEETLE_SPRITE_PATH_RED = None
BEETLE_SCALING = .65

class BeetleBattle(arcade.Window):
    def __init__(self):

        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.beetle_sprite_list = None
        self.beetle_prototype = None
        self.background = None

        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        self.background = arcade.load_texture("Assets/Images/octagon.png")

        self.beetle_sprite_list = arcade.SpriteList()

        # Set up the beetle and place it at these coordinates
        self.beetle_prototype = arcade.Sprite(BEETLE_SPRITE_PATH_GREEN, BEETLE_SCALING)
        self.beetle_prototype.center_x = 70
        self.beetle_prototype.center_y = 65
        self.beetle_sprite_list.append(self.beetle_prototype)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.beetle_sprite_list.draw()


if __name__ == "__main__":
    app = BeetleBattle()
    app.setup()
    arcade.run()