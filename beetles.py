import arcade
import math
import random
from team_color import TeamColor

BEETLE_SPRITE_PATH_GREEN = "Assets/Sprites/beetle1_GREEN.png"
BEETLE_SPRITE_PATH_RED = "Assets/Sprites/beetle1_RED.png"
BEETLE_SCALING = 1
BEETLE_MOVE_FORCE = 500

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
        self.scale = BEETLE_SCALING
        self.team_color = team_color
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
        self.force = 0
        self.target_facing = None
        self.target_moving = None
        self.is_moving = None
        self.x_velocity = 0
        self.y_velocity = 0

    @property
    def physics_engine(self):
        return self.physics_engines[0]
    
    def move_to(self, click_x, click_y):
        delta_x = click_x - self.center_x
        delta_y = click_y - self.center_y
        reached_target = delta_x < 10 and delta_y < 10
        self.angle = math.atan2(delta_y, delta_x)
        self.x_velocity = math.sin(self.radians) * BEETLE_MOVE_FORCE
        self.y_velocity = math.cos(self.radians) * BEETLE_MOVE_FORCE
        self.move_vector = (self.x_velocity, self.y_velocity)

        if reached_target is False:
            self.is_moving = True
        elif reached_target is True:
            self.is_moving = False
        else:
            self.is_moving = None
        return self.is_moving

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
        if self.hit_points <= 0:
            self.remove_from_sprite_lists()

        if self.is_moving is True:
            self.physics_engine.apply_force(self, (self.x_velocity, self.y_velocity))
        else:
            self.physics_engine.set_velocity(self, (0, 0))

    def damage(self, damage):
        self.hit_points -= damage