import arcade
from team_color import TeamColor

# TODO: Move these to a shared file so I don't have to copy them
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WINDOW_FUDGE_FACTOR = 50.0
MIN_X = -WINDOW_FUDGE_FACTOR
MAX_X = SCREEN_WIDTH + WINDOW_FUDGE_FACTOR
MIN_Y = -WINDOW_FUDGE_FACTOR
MAX_Y = SCREEN_HEIGHT + WINDOW_FUDGE_FACTOR

class Hazard(arcade.Sprite):
    def __init__(self, path, center_x, center_y, scaling=1.0, team_color=TeamColor.NEUTRAL):
        super().__init__(path, scaling)
        self.center_x = center_x
        self.center_y = center_y
        self.team_color = team_color
        self.active = True
        self.spatial_manager = None

    @property
    def physics_engine(self):
        if len(self.physics_engines) > 0:
            return self.physics_engines[0]
        else:
            return None

    def draw(self):
        # TODO: handle drawing the hazard
        super().draw()

    def on_update(self, delta_time):
        # TODO: Called every frame, will be used to update the hazard, performing its actions during battle
        super().on_update(delta_time)

class Projectile(Hazard):
    def __init__(self, path, center_x, center_y, angle, power=0, scaling=1.0, team_color=TeamColor.NEUTRAL):
        super().__init__(path, center_x, center_y, scaling, team_color)
        self.angle = angle
        self.power = power
        self.forward_speed = 0.0
        self.sideways_speed = 0.0

    def draw(self):
        # TODO: handle drawing the projectile
        super().draw()

    def on_update(self, delta_time):
        # TODO: Called every frame, will be used to update the projectile, performing its actions during battle
        super().on_update(delta_time)
        if self.center_x <= __class__.MIN_X or self.center_x >= __class__.MAX_X:
            self.remove_from_sprite_lists()
            self.spatial_manager.remove(self)
            self.active = False
        elif self.center_y <= __class__.MIN_Y or self.center_y >= __class__.MAX_Y:
            self.remove_from_sprite_lists()
            self.spatial_manager.remove(self)
            self.active = False

class PincerExecution(Hazard):
    def __init__(self, path, center_x, center_y, angle, power=0, scaling=1.0, team_color=TeamColor.NEUTRAL):
        super().__init__(path, center_x, center_y, scaling, team_color)
        self.angle = angle
        self.power = power
        self.forward_speed = 0.0
        self.sideways_speed = 0.0

    def draw(self):
        # TODO: handle drawing the projectile
        super().draw()

    def on_update(self, delta_time):
        # TODO: Called every frame, will be used to update the projectile, performing its actions during battle
        super().on_update(delta_time)
        if self.center_x <= __class__.MIN_X or self.center_x >= __class__.MAX_X:
            self.remove_from_sprite_lists()
            self.spatial_manager.remove(self)
            self.active = False
        elif self.center_y <= __class__.MIN_Y or self.center_y >= __class__.MAX_Y:
            self.remove_from_sprite_lists()
            self.spatial_manager.remove(self)
            self.active = False