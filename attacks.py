import math
from sound_manager import SoundManager
from abilities import Ability
from hazards import Projectile
from traits import Trait
from team_color import TeamColor

DEFAULT_POWER = 1
DEFAULT_FIRE_RATE = 20.0
DEFAULT_RANGE = 500.0
PROJECTILE_MOVE_FORCE = 2500
PROJECTILE_SCALING = 1

sound_manager = SoundManager()

class Attack(Ability):
    def __init__(self, acting_beetle):
        super().__init__(acting_beetle)
        self.power = DEFAULT_POWER
        self.fire_rate = DEFAULT_FIRE_RATE
        self.range = DEFAULT_RANGE
        self.number_of_attacks = 1
        self.time_since_last = 0.0

    def draw(self):
        super().draw()
        # TODO: Draw the attack

    def on_update(self, delta_time):
        super().on_update(delta_time)
        # TODO: To perform the atack with given beetle during each frame, if needed
        self.time_since_last += delta_time

class RangedAttack(Attack):
    def __init__(self, acting_beetle):
        super().__init__(acting_beetle)

    def draw(self):
        super().draw()
        # TODO: Draw the attack

    def on_update(self, delta_time):
        super().on_update(delta_time)
        # check the cooldown from the acting beetle
        # if ready, generate a new Projectile class
        # otherwise, do nothing
        # TODO: To perform the atack with given beetle during each frame, if needed

class Peashooter(RangedAttack):
    PEASHOOTER_COOLDOWN = 0.5

    def __init__(self, acting_beetle):
        super().__init__(acting_beetle)

    def draw(self):
        super().draw()
        # TODO: Draw the attack

    def on_update(self, delta_time):
        super().on_update(delta_time)
        beetle = self.acting_beetle
        if self.ready_to_fire:
            angle = beetle.get_sprite_adjusted_angle_deg(beetle.angle)
            if beetle.firing_target:
                x, y = beetle.firing_target
                x_distance = x - beetle.center_x
                y_distance = y - beetle.center_y
                angle = math.degrees(math.atan2(y_distance, x_distance))

            projectile = __class__.projectile(beetle.center_x, beetle.center_y, angle, beetle)
            beetle.team.projectiles_list.append(projectile)
            beetle.physics_engine.add_sprite(projectile, elasticity = 0.1, collision_type = "pea")
            beetle.spatial_manager.add_sprite(projectile)
            self.cooldown = __class__.PEASHOOTER_COOLDOWN

    class trait(Trait):
        def __init__(self):
            super().__init__(Peashooter)

    class projectile(Projectile):
        SPRITE_PATH_GREEN = "Assets/Sprites/Attributed/bullet_bw_green.png"
        SPRITE_PATH_RED = "Assets/Sprites/Attributed/bullet_bw_red.png"
        DEFAULT_PEA_VELOCITY_MULTIPLIER = 1000.0
        PEA_POWER = 1

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
            sound_manager.play_sound("PeashooterPew")

        def draw(self):
            super().draw()
            # TODO: Draw the attack

        def on_update(self, delta_time):
            super().on_update(delta_time)
            if self.active:
                self.physics_engine.set_velocity(self, (self.shot_vector[0], self.shot_vector[1]))
