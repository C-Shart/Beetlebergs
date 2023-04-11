import math
from abilities import Ability
from hazards import Projectile
from traits import Trait
from team_color import TeamColor

DEFAULT_POWER = 1
DEFAULT_FIRE_RATE = 20.0
DEFAULT_RANGE = 500.0
PROJECTILE_MOVE_FORCE = 2500
PROJECTILE_SCALING = 1

class Attack(Ability):
    def __init__(self, acting_beetle):
        super().__init__(acting_beetle)
        self.power = DEFAULT_POWER
        self.fire_rate = DEFAULT_FIRE_RATE
        self.range = DEFAULT_RANGE
        self.number_of_attacks = 1
        self.time_since_last = 0.0

    def on_draw(self):
        super().on_draw()
        # TODO: Draw the attack

    def on_update(self, delta_time):
        super().on_update(delta_time)
        # TODO: To perform the atack with given beetle during each frame, if needed
        self.time_since_last += delta_time

class RangedAttack(Attack):
    def __init__(self, acting_beetle):
        super().__init__(acting_beetle)

    def on_draw(self):
        super().on_draw()
        # TODO: Draw the attack

    def on_update(self, delta_time):
        super().on_update(delta_time)
        # check the cooldown from the acting beetle
        # if ready, generate a new Projectile class
        # otherwise, do nothing
        # TODO: To perform the atack with given beetle during each frame, if needed

class Peashooter(RangedAttack):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        super().on_draw()
        # TODO: Draw the attack

    def on_update(self, delta_time):
        super().on_update(delta_time)
        # TODO: To perform the atack with given beetle during each frame, if needed

    class trait(Trait):
        def __init__(self):
            super().__init__(Peashooter)

    class projectile(Projectile):
        SPRITE_PATH_GREEN = "Assets/Sprites/Attributed/bullet_bw_green.png"
        SPRITE_PATH_RED = "Assets/Sprites/Attributed/bullet_bw_red.png"
        DEFAULT_PEA_VELOCITY_MULTIPLIER = 500.0
        PEA_POWER = 20

        def __init__(self, center_x, center_y, angle, acting_beetle):
            path = __class__.SPRITE_PATH_GREEN
            if acting_beetle.team.color != TeamColor.GREEN:
                path = __class__.SPRITE_PATH_RED
            super().__init__(path, center_x, center_y, angle, __class__.PEA_POWER, team_color=acting_beetle.team.color)
            self.angle = angle

            x_velocity = math.cos(self.radians) * __class__.DEFAULT_PEA_VELOCITY_MULTIPLIER
            y_velocity = math.sin(self.radians) * __class__.DEFAULT_PEA_VELOCITY_MULTIPLIER
            self.shot_vector = (x_velocity, y_velocity)

            # Fixes the angle of the sprite itself, avoiding changing the velocity vector
            self.angle -= 90.0

        def on_draw(self):
            super().on_draw()
            # TODO: Draw the attack

        def on_update(self, delta_time):
            super().on_update(delta_time)
            self.physics_engine.set_velocity(self, (self.shot_vector[0], self.shot_vector[1]))