import arcade
import math
import random
from team_color import TeamColor

BEETLE_SPRITE_PATH_GREEN = "Assets/Sprites/beetle1_GREEN.png"
BEETLE_SPRITE_PATH_RED = "Assets/Sprites/beetle1_RED.png"
BEETLE_SCALING = 1
BEETLE_MOVE_FORCE = 4000

DEFAULT_HIT_POINTS = 100
DEFAULT_MAX_FORWARD = 5.0
DEFAULT_MAX_SIDEWAYS = 2.5
DEFAULT_MAX_ROTATION = math.pi / 360.0
DEFAULT_AWARENESS = 50
DEFAULT_VISION = 25
DEFAULT_ACCURACY = 25

class Beetle(arcade.Sprite):
    def __init__(self, team_color, center_x, center_y):
        path = BEETLE_SPRITE_PATH_GREEN if team_color == TeamColor.GREEN else BEETLE_SPRITE_PATH_RED
        super().__init__(path, BEETLE_SCALING)
        self.center_x = center_x
        self.center_y = center_y
        self.abilities = []
        self.max_hit_points = DEFAULT_HIT_POINTS
        self.hit_points = DEFAULT_HIT_POINTS
        self.max_forward_speed = DEFAULT_MAX_FORWARD
        self.forward_speed = 0.0
        self.max_sideways_speed = DEFAULT_MAX_SIDEWAYS
        self.sideways_speed = 0.0
        self.max_rotation_speed = DEFAULT_MAX_ROTATION
        self.awareness = DEFAULT_AWARENESS
        self.vision = DEFAULT_VISION
        self.accuracy = DEFAULT_ACCURACY
        self.angle = 270.0 if team_color == TeamColor.GREEN else 90.0

    def on_draw(self):
        # TODO: handle drawing the beetle
        super().on_draw()
        for ability in self.abilities:
            ability.on_draw()

    def on_update(self, delta_time):
        # TODO: Called every frame, will be used to update the beetle, performing its actions during battle
        super().on_update(delta_time)
        for ability in self.abilities:
            ability.on_update(delta_time, self)