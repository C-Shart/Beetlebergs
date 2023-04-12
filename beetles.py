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
        self.facing_cooldown = 0.0
        self.firing_target = None
        self.known_enemies = None
        self.active = False

    @property
    def physics_engine(self):
        if len(self.physics_engines) > 0:
            return self.physics_engines[0]
        else:
            return None

    def get_sprite_adjusted_angle_deg(_self, angle):
        angle += 90.0 # TODO: Why is this one plus?
        if angle < -180.0:
            angle += 360.0
        return angle

    def get_sprite_adjusted_angle_rad(_self, angle):
        angle -= math.pi / 2.0
        if angle < -math.pi:
            angle += math.pi * 2.0
        return angle

    def get_angle_to_location(self, target_x, target_y):
        delta_x = target_x - self.center_x
        delta_y = target_y - self.center_y
        return self.get_sprite_adjusted_angle_rad(math.atan2(delta_y, delta_x))

    def decide_facing(self, delta_time):
        if not self.angle_target and self.facing_cooldown <= 0.0:
            self.facing_cooldown = 0.0
            self.angle_target = random.uniform(-math.pi, math.pi)
        elif self.facing_cooldown > 0.0:
            self.facing_cooldown -= delta_time

    def decide_position(self):
        if not self.move_target:
            self.move_target = (random.randrange(0, 1280), random.randrange(0, 720))

    def set_facing(self, target_x, target_y):
        self.angle_target = self.get_angle_to_location(target_x, target_y)

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
        if self.active:
            self.decide_facing(delta_time)
            self.decide_position()

        for ability in self.abilities:
            ability.on_update(delta_time)
            ability.active = self.active

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
                    self.angle_target = None
                    self.facing_cooldown = 1.0
                elif delta_rotation >= 0.0:
                    body.angle += min(delta_rotation, BEETLE_ROTATION_SPEED)
                else:
                    body.angle += max(delta_rotation, -BEETLE_ROTATION_SPEED)
                pass

    def damage(self, damage):
        self.hit_points -= damage