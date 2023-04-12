import arcade
import math
import random
from team_color import TeamColor

BEETLE_SPRITE_PATH_GREEN = "Assets/Sprites/beetle1_GREEN.png"
BEETLE_SPRITE_PATH_RED = "Assets/Sprites/beetle1_RED.png"
BEETLE_SCALING = 1
BEETLE_MOVE_FORCE = 500
BEETLE_ROTATION_SPEED = math.pi / 8.0

DEFAULT_HIT_POINTS = 100
DEFAULT_MAX_FORWARD = 150.0
DEFAULT_MAX_SIDEWAYS = 100.0
DEFAULT_MAX_ROTATION = math.pi / 360.0
DEFAULT_AWARENESS = 1
DEFAULT_VISION = 250
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
        self.angle = -90.0 if team.color == TeamColor.GREEN else 90.0
        self.force = 0
        self.target_facing = None
        self.target_moving = None
        self.is_moving = None
        self.x_velocity = 0
        self.y_velocity = 0
        self.move_target = None
        self.angle_target = None
        self.firing_target = None
        self.known_enemies = None

    @property
    def physics_engine(self):
        if len(self.physics_engines) > 0:
            return self.physics_engines[0]
        else:
            return None

    def get_angle_to_location(self, target_x, target_y):
        delta_x = target_x - self.center_x
        delta_y = target_y - self.center_y
        angle = math.atan2(delta_y, delta_x) - math.pi / 2.0
        if angle < -math.pi:
            angle += math.pi * 2.0
        return angle

    def set_facing(self, target_x = 640, target_y = 360, enemy_x = None, enemy_y = None):
        focus_x = target_x if enemy_x is None else enemy_x
        focus_y = target_y if enemy_y is None else enemy_y
        self.angle_target = self.get_angle_to_location(focus_x, focus_y)

    def move_to(self, target_x, target_y):
        self.move_target = (target_x, target_y)
        # TODO: Do we need this anymore if we're just setting move_target?

    def draw(self):
        # TODO: handle drawing the beetle
        super().draw()
        for ability in self.abilities:
            ability.draw()
        # FOR TESTING PURPOSES
        arcade.draw_circle_outline(self.center_x, self.center_y, DEFAULT_VISION, arcade.color.ELECTRIC_PURPLE, 2)

    def on_update(self, delta_time):
        # TODO: Called every frame, will be used to update the beetle, performing its actions during battle
        super().on_update(delta_time)
        for ability in self.abilities:
            ability.on_update(delta_time)
        if self.hit_points <= 0:
            self.remove_from_sprite_lists()
        else:
            if self.move_target:
                target_x, target_y = self.move_target
                delta_x = target_x - self.center_x
                delta_y = target_y - self.center_y
                if abs(delta_x) < 10.0 and abs(delta_y) < 10.0:
                    self.move_target = None
                    self.physics_engine.set_velocity(self, (0.0 , 0.0))
                else:
                    target_angle = math.atan2(delta_y, delta_x)
                    x_velocity = math.cos(target_angle) * BEETLE_MOVE_FORCE
                    y_velocity = math.sin(target_angle) * BEETLE_MOVE_FORCE
                    self.physics_engine.set_velocity(self, (x_velocity, y_velocity))

            if self.angle_target:
                body = self.physics_engine.sprites[self].body
                delta_rotation = self.angle_target - body.angle
                if abs(delta_rotation) < 0.0000005:
                    self.target_angle = None
                elif delta_rotation >= 0.0:
                    body.angle += min(delta_rotation, BEETLE_ROTATION_SPEED)
                else:
                    body.angle += max(delta_rotation, -BEETLE_ROTATION_SPEED)
                pass

    def damage(self, damage):
        self.hit_points -= damage