import arcade
from team_color import TeamColor

class Hazard(arcade.Sprite):
    def __init__(self, path, center_x, center_y, scaling=1.0, team_color=TeamColor.NEUTRAL):
        super().__init__(path, scaling)
        self.center_x = center_x
        self.center_y = center_y
        self.team_color = team_color

    @property
    def physics_engine(self):
        return self.physics_engines[0]

    def on_draw(self):
        # TODO: handle drawing the hazard
        super().on_draw()

    def on_update(self, delta_time):
        # TODO: Called every frame, will be used to update the hazard, performing its actions during battle
        super().on_update(delta_time)

class Projectile(Hazard):
    def __init__(self, path, center_x, center_y, angle, scaling=1.0, team_color=TeamColor.NEUTRAL):
        super().__init__(path, center_x, center_y, scaling, team_color)
        self.angle = angle
        self.forward_speed = 0.0
        self.sideways_speed = 0.0

    def on_draw(self):
        # TODO: handle drawing the projectile
        super().on_draw()

    def on_update(self, delta_time):
        # TODO: Called every frame, will be used to update the projectile, performing its actions during battle
        super().on_update(delta_time)