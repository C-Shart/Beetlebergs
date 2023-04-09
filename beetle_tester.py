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

        def hit_handler(sprite_a, sprite_b, arbiter, space, data):
            sprite_shape = arbiter.shapes[0]
            sprite = self.physics_engine.get_sprite_for_shape(sprite_shape)
            sprite.remove_from_sprite_lists()

        def nohit_handler(sprite_a, sprite_b, arbiter, space, data):
            
            pass

        self.physics_engine.add_collision_handler("pea", "beetle", hit_handler)
        self.physics_engine.add_collision_handler("pea", "pea", nohit_handler)

    def on_mouse_press(self, x, y, button, modifiers):
        beetle = self.green_team.beetles[0] if button == arcade.MOUSE_BUTTON_LEFT else self.red_team.beetles[0]
        x_distance = x - beetle.center_x
        y_distance = y - beetle.center_y
        angle = (math.degrees(math.atan2(y_distance, x_distance)))
        projectile = attacks.Peashooter.projectile(beetle.center_x, beetle.center_y, angle, beetle)
        self.projectiles_list.append(projectile)
        self.physics_engine.add_sprite_list(self.projectiles_list,
            collision_type = "pea",
            elasticity = 0.1
        )
        # TODO: Figure out how to decouple the sprite angle & the shot angle. Currently sprites are rotated 270 degrees
        # from their flight path.

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