import arcade
from attacks import Peashooter
from beetles import Beetle, DEFAULT_HIT_POINTS

class Team:
    def __init__(self, color, center_x, center_y):
        self.color = color
        self.center_x = center_x
        self.center_y = center_y
        self.beetles = [Beetle(self, self.center_x, self.center_y)]
        self.sprite_list = arcade.SpriteList()
        self.projectiles_list = arcade.SpriteList()
        self.traits = [Peashooter.trait()] # TODO: Add more traits at random

        for beetle in self.beetles:
            self.sprite_list.append(beetle)

    def set_up_team(self):
        beetle_ability_traits = []
        for trait in self.traits:
            if trait.ability is None:
                trait.set_up_trait(self)
            else:
                beetle_ability_traits.append(trait)

        for beetle in self.beetles:
            beetle.hit_points = DEFAULT_HIT_POINTS
            beetle.abilities = []
            for trait in beetle_ability_traits:
                beetle.abilities.append(trait.ability(beetle))
            # TODO: Reset positions
            # TODO: Randomize positions? (i.e. randomized positions within a group on each side)


    def on_draw(self):
        # TODO: Draws the team
        self.sprite_list.draw()
        self.projectiles_list.draw()

    def on_update(self, delta_time):
        self.sprite_list.on_update(delta_time)
        self.projectiles_list.on_update(delta_time)