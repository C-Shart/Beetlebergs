import arcade

BEETLE_SPRITE_PATH_GREEN = "Assets/Sprites/beetle1_GREEN.png"
BEETLE_SPRITE_PATH_RED = "Assets/Sprites/beetle1_RED.png"
BEETLE_SCALING = 1

class Beetle(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__(BEETLE_SPRITE_PATH_GREEN, BEETLE_SCALING)
        self.center_x = center_x
        self.center_y = center_y