from abilities import Ability
from traits import Trait

DEFAULT_POWER = 1
DEFAULT_FIRE_RATE = 1.0
DEFAULT_RANGE = 500.0

class Attack(Ability):
    def __init__(self):
        super().__init__(self)
        self.power = DEFAULT_POWER
        self.fire_rate = DEFAULT_FIRE_RATE
        self.range = DEFAULT_RANGE
        self.number_of_attacks = 1

    def on_draw(self):
        super().on_draw(self)
        # TODO: Draw the attack
        pass

    def on_update(self, delta_time, acting_beetle):
        super().on_update(self, delta_time, acting_beetle)
        # TODO: To perform the atack with given beetle during each frame, if needed
        pass

class RangedAttack(Attack):
    def __init__(self):
        super().__init__(self)

    def on_draw(self):
        super().on_draw(self)
        # TODO: Draw the attack
        pass

    def on_update(self, delta_time, acting_beetle):
        super().on_update(self, delta_time, acting_beetle)
        # TODO: To perform the atack with given beetle during each frame, if needed
        pass

class Peashooter(RangedAttack):
    def __init__(self):
        super().__init__(self)

    def on_draw(self):
        super().on_draw(self)
        # TODO: Draw the attack
        pass

    def on_update(self, delta_time, acting_beetle):
        super().on_update(self, delta_time, acting_beetle)
        # TODO: To perform the atack with given beetle during each frame, if needed
        pass

class PeashooterTrait(Trait):
    def __init__(self):
        super().__init__(self)
        self.ability = Peashooter
