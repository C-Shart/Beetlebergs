import arcade
import attacks
import math
from teams import Team
from team_color import TeamColor

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
        self.projectiles_list = None

        self.green_team = None
        self.red_team = None

        self.physics_engine = None

    def setup(self):
        self.background = arcade.load_texture("Assets/Images/octagon.png")
        self.projectiles_list = arcade.SpriteList()

        self.green_team = Team(TeamColor.GREEN, 320, 260)
        self.green_team.set_up_team()

        self.red_team = Team(TeamColor.RED, 960, 260)
        self.red_team.set_up_team()

        self.physics_engine = arcade.PymunkPhysicsEngine()

    def on_mouse_press(self, x, y, button, modifiers):
        beetle = self.green_team.beetles[0] if button == arcade.MOUSE_BUTTON_LEFT else self.red_team.beetles[0]
        x_distance = x - beetle.center_x
        y_distance = y - beetle.center_y
        angle = (math.degrees(math.atan(y_distance / x_distance))) - 90
        projectile = attacks.Peashooter.projectile(beetle.center_x, beetle.center_y, angle, beetle)
        self.projectiles_list.append(projectile)
        self.physics_engine.add_sprite(projectile)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.green_team.on_draw()
        self.red_team.on_draw()
        self.projectiles_list.draw()

    def on_update(self, delta_time):
        self.green_team.on_update(delta_time)
        self.red_team.on_update(delta_time)
        self.projectiles_list.on_update(delta_time)
        self.physics_engine.step()

if __name__ == "__main__":
    app = BeetleTestes()
    app.setup()
    arcade.run()