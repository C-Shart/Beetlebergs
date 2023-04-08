import arcade
from typing import Optional
from beetles import Beetle
from teams import Team
from team_color import TeamColor
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "BIG BAD BEETLE BALLS"

class BeetleTestes(arcade.Window):
    def __init__(self):
        # Call the parent class constructor
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.WHITE)

        self.background = None
        self.green_team = None
        self.red_team = None
        self.green_attacks = None
        self.red_attacks = None

        self.green_tester = None
        self.red_tester = None

        self.physics_engine: Optional[PymunkPhysicsEngine] = None

    def setup(self):
        self.background = arcade.load_texture("Assets/Images/octagon.png")

        self.green_team = Team(TeamColor.GREEN, 320, 260)
        self.green_team.set_up_team()
        self.red_team = Team(TeamColor.RED, 960, 260)
        self.red_team.set_up_team()

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """
        # TODO: Set navigation points by clicking the mouse
        # Eventually we would hand this off to the AI to set.
        pass

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.green_team.on_draw()
        self.red_team.on_draw()

    def on_update(self, delta_time):
        self.green_team.on_update(delta_time)
        self.red_team.on_update(delta_time)

if __name__ == "__main__":
    app = BeetleTestes()
    app.setup()
    arcade.run()