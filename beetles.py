import arcade
import math
import random
from team_color import TeamColor

BEETLE_SPRITE_PATH_GREEN = "Assets/Sprites/beetle1_GREEN.png"
BEETLE_SPRITE_PATH_RED = "Assets/Sprites/beetle1_RED.png"
BEETLE_SCALING = 1
BEETLE_MOVE_FORCE = 500

DEFAULT_HIT_POINTS = 100
DEFAULT_MAX_FORWARD = 150.0
DEFAULT_MAX_SIDEWAYS = 100.0
DEFAULT_MAX_ROTATION = math.pi / 360.0
DEFAULT_AWARENESS = 50
DEFAULT_VISION = 25
DEFAULT_ACCURACY = 25

class Beetle(arcade.Sprite):
    def __init__(self, team, center_x, center_y):
        path = BEETLE_SPRITE_PATH_GREEN if team.color == TeamColor.GREEN else BEETLE_SPRITE_PATH_RED
        super().__init__(path, BEETLE_SCALING)
        self.team = team
        self.scale = BEETLE_SCALING
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
        self.angle = 270.0 if team.color == TeamColor.GREEN else 90.0
        self.force = 0
        self.target_facing = None
        self.target_moving = None
        self.is_moving = None
        self.x_velocity = 0
        self.y_velocity = 0
        self.firing_target = None
    @property
    def physics_engine(self):
        if len(self.physics_engines) > 0:
            return self.physics_engines[0]
        else:
            return None

    def move_to(self, click_x, click_y):
        delta_x = click_x - self.center_x
        delta_y = click_y - self.center_y
        reached_target = delta_x < 50 and delta_y < 50
        self.angle = math.atan2(delta_y, delta_x)

        self.xtest = math.sin(self.angle) * BEETLE_MOVE_FORCE
        self.ytest = math.cos(self.angle) * BEETLE_MOVE_FORCE

        self.x_velocity = math.sin(self.radians) * BEETLE_MOVE_FORCE
        self.y_velocity = math.cos(self.radians) * BEETLE_MOVE_FORCE

        self.move_vector = (self.xtest, self.ytest)

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
            ability.on_update(delta_time)
        if self.hit_points <= 0:
            self.remove_from_sprite_lists()

        if self.is_moving is True:
            self.physics_engine.apply_force(self, self.move_vector)
        else:
            self.physics_engine.set_velocity(self, (0, 0))

    def damage(self, damage):
        self.hit_points -= damage