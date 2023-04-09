import arcade
from attacks import Peashooter
from beetles import Beetle, DEFAULT_HIT_POINTS

class Team:
    def __init__(self, color, center_x, center_y):
        self.color = color
        self.center_x = center_x
        self.center_y = center_y
        self.beetles = [Beetle(self.color, self.center_x, self.center_y)]
        self.sprite_list = arcade.SpriteList()
        self.traits = [Peashooter.trait()] # TODO: Add more traits at random

        for beetle in self.beetles:
            self.sprite_list.append(beetle)

    def set_up_team(self):
        # TODO: Responsible for preparing the beetles for battle, refreshing their health, resetting their positions.
        beetle_abilities = []
        for trait in self.traits:
            if trait.ability is None:
                beetle_abilities.append(trait.ability())
            else:
                trait.set_up_trait(self)

        for beetle in self.beetles:
            beetle.hit_points = DEFAULT_HIT_POINTS
            beetle.abilities = beetle_abilities
            # TODO: Reset positions
            
            # TODO: Randomize positions? (i.e. randomized positions within a group on each side)


    def on_draw(self):
        # TODO: Draws the team
        self.sprite_list.draw()

    def on_update(self, delta_time):
        # TODO: Updates the team
        for beetle in self.beetles:
            beetle.on_update(delta_time)