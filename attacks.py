import arcade
import math
import random
from abilities import Ability
from traits import Trait

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
        pass

    def on_update(self, delta_time, acting_beetle):
        super().on_update(delta_time, acting_beetle)
        # TODO: To perform the atack with given beetle during each frame, if needed
        pass

class RangedAttack(Attack):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        super().on_draw()
        # TODO: Draw the attack
        pass

    def on_update(self, delta_time, acting_beetle):
        super().on_update(delta_time, acting_beetle)
        # TODO: To perform the atack with given beetle during each frame, if needed
        pass

class Peashooter(RangedAttack):
    def __init__(self):
        super().__init__()
        self.time_between = DEFAULT_FIRE_RATE
        self.time_since_last = 0.0
        self.peashooter_list = []

    def on_draw(self):
        super().on_draw()
        # TODO: Draw the attack
        pass

    def on_update(self, delta_time, acting_beetle):
        super().on_update(delta_time, acting_beetle)
        # TODO: To perform the atack with given beetle during each frame, if needed
        self.time_since_last += delta_time
        if self.time_since_last >= self.time_between:
            self.time_since_last = 0
            pea = arcade.Sprite(PEA_GRN_SPRITEPATH)
            pea.center_x = self.center_x
            pea.angle = 270
            pea.change_x = 5
            self.peashooter_list.append(pea)

        pass

    class trait(Trait):
        def __init__(self):
            super().__init__(Peashooter)
