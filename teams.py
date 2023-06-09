import arcade
from attacks import Peashooter
from beetles import Beetle, DEFAULT_HIT_POINTS
from team_color import TeamColor

TEAM_CELL_SIZE = 100
TEAM_CELL_OFFSETS = [
    (0, 0), (0, TEAM_CELL_SIZE), (0, -TEAM_CELL_SIZE), (0, 2 * TEAM_CELL_SIZE), (0, -2 * TEAM_CELL_SIZE),
    (2 * TEAM_CELL_SIZE, 0), (2 * TEAM_CELL_SIZE, TEAM_CELL_SIZE), (2 * TEAM_CELL_SIZE, -TEAM_CELL_SIZE),
    (2 * TEAM_CELL_SIZE, 2 * TEAM_CELL_SIZE), (2 * TEAM_CELL_SIZE, -2 * TEAM_CELL_SIZE)
    ]

class Team:
    def __init__(self, color, center_x, center_y):
        self.color = color
        self.center_x = center_x
        self.center_y = center_y
        self.beetles = [Beetle(self, self.center_x, self.center_y)]
        self.sprite_list = arcade.SpriteList()
        self.projectiles_list = arcade.SpriteList()
        self.traits = [Peashooter.trait()] # TODO: Add more traits at random
        self.active = False
        self.other_team = None

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        for beetle in self.beetles:
            beetle.active = value
            if not value:
                beetle.move_target = None
                beetle.physics_engine and beetle.physics_engine.set_velocity(beetle, (0.0, 0.0))
                for ability in beetle.abilities:
                    ability.active = False
        self._active = value

    def set_up_team(self):
        self.active = False
        self.sprite_list.clear()
        self.projectiles_list.clear()

        for beetle in self.beetles:
            self.sprite_list.append(beetle)

        beetle_ability_traits = []
        for trait in self.traits:
            if trait.ability is None:
                trait.set_up_trait(self)
            else:
                beetle_ability_traits.append(trait)

        current_offset = 0
        for beetle in self.beetles:
            beetle.hit_points = DEFAULT_HIT_POINTS
            beetle.abilities = []

            # TODO: Randomize positions? (i.e. randomized positions within a group on each side)
            offset_x, offset_y = TEAM_CELL_OFFSETS[current_offset] # TODO: Will run out after 10 beetles!
            offset_x = offset_x if self.color == TeamColor.RED else -offset_x
            beetle.center_x = self.center_x + offset_x
            beetle.center_y = self.center_y + offset_y
            current_offset += 1

            beetle.angle = -90.0 if self.color == TeamColor.GREEN else 90.0
            for trait in beetle_ability_traits:
                beetle.abilities.append(trait.ability(beetle))

    def on_draw(self):
        for beetle in self.sprite_list:
            beetle.draw()
        self.sprite_list.draw()
        for projectile in self.projectiles_list:
            projectile.draw()
        self.projectiles_list.draw()

    def on_update(self, delta_time):
        self.sprite_list.on_update(delta_time)
        self.projectiles_list.on_update(delta_time)