import arcade
from abilities import Ability
from hazards import Projectile
from traits import Trait
from team_color import TeamColor

DEFAULT_POWER = 1
DEFAULT_FIRE_RATE = 20.0
DEFAULT_RANGE = 500.0
PROJECTILE_MOVE_FORCE = 2500
PROJECTILE_SCALING = 1
PEA_GRN_SPRITEPATH = "Assets\Sprites\Attributed\bullet_bw_green.png"
PEA_RED_SPRITEPATH = "Assets\Sprites\Attributed\bullet_bw_red.png"

class Attack(Ability):
    def __init__(self):
        super().__init__()
        self.power = DEFAULT_POWER
        self.fire_rate = DEFAULT_FIRE_RATE
        self.range = DEFAULT_RANGE
        self.number_of_attacks = 1

    def on_draw(self):
        super().on_draw()
        # TODO: Draw the attack

    def on_update(self, delta_time, acting_beetle):
        super().on_update(delta_time, acting_beetle)
        # TODO: To perform the atack with given beetle during each frame, if needed

class RangedAttack(Attack):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        super().on_draw()
        # TODO: Draw the attack

    def on_update(self, delta_time, acting_beetle):
        super().on_update(delta_time, acting_beetle)
        # TODO: To perform the atack with given beetle during each frame, if needed

class Peashooter(RangedAttack):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        super().on_draw()
        # TODO: Draw the attack

    def on_update(self, delta_time, acting_beetle):
        super().on_update(delta_time, acting_beetle)
        # TODO: To perform the atack with given beetle during each frame, if needed

    class trait(Trait):
        def __init__(self):
            super().__init__(Peashooter)
