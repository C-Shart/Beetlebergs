class Ability:
    def __init__(self, acting_beetle):
        self.acting_beetle = acting_beetle
        self.enabled = False
        self.cooldown = 0.0

    @property
    def ready_to_fire(self):
        return self.enabled and self.cooldown <= 0.0

    def draw(self):
        # TODO: Draw the ability
        pass

    def on_update(self, delta_time):
        if self.cooldown > 0.0:
            self.cooldown -= delta_time