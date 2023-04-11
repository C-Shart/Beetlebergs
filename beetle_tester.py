import arcade
import arcade.gui
import attacks
from enum import Enum
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

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.settings_box = arcade.gui.UIBoxLayout()

        self.mode = __class__.TesterMode.SHOOTING
        self.mode_button = arcade.gui.UIFlatButton(text="Shooting", width=200)
        self.mode_button.on_click = self.on_click_mode

        self.settings_box.add(self.mode_button.with_space_around(bottom=20))
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="top", child=self.settings_box))

    def setup(self):
        self.background = arcade.load_texture("Assets/Images/octagon.png")
        self.projectiles_list = arcade.SpriteList()

        self.green_team = Team(TeamColor.GREEN, 320, 260)
        self.green_team.set_up_team()

        self.red_team = Team(TeamColor.RED, 960, 260)
        self.red_team.set_up_team()

        self.physics_engine = arcade.PymunkPhysicsEngine()

        self.physics_engine.add_sprite_list(self.green_team.beetles,
                    elasticity = 0.0,
                    friction = 0.8,
                    moment_of_intertia = 1,
                    collision_type="green_beetle"
                    )
        self.physics_engine.add_sprite_list(self.red_team.beetles,
                    elasticity = 0.0,
                    friction = 0.8,
                    moment_of_intertia = 1,
                    collision_type="red_beetle"
                    )

        def hit_handler(sprite_a, sprite_b, arbiter, space, data):
            first_shape = arbiter.shapes[0]
            second_shape = arbiter.shapes[1]
            sprite = self.physics_engine.get_sprite_for_shape(second_shape) if first_shape == "pea" else self.physics_engine.get_sprite_for_shape(first_shape)
            sprite.remove_from_sprite_lists()
            return True

        def nohit_handler(sprite_a, sprite_b, arbiter, space, data):
            return False

        self.physics_engine.add_collision_handler("green_pea", "green_beetle", nohit_handler)
        self.physics_engine.add_collision_handler("red_pea", "green_beetle", hit_handler)
        self.physics_engine.add_collision_handler("green_pea", "red_beetle", hit_handler)
        self.physics_engine.add_collision_handler("red_pea", "red_beetle", nohit_handler)

        self.physics_engine.add_collision_handler("pea", "pea", nohit_handler)

    def on_mouse_press(self, x, y, button, modifiers):
        beetle = self.green_team.beetles[0] if button == arcade.MOUSE_BUTTON_LEFT else self.red_team.beetles[0]
        if self.mode == __class__.TesterMode.SHOOTING:
            x_distance = x - beetle.center_x
            y_distance = y - beetle.center_y
            angle = (math.degrees(math.atan2(y_distance, x_distance)))
            projectile = attacks.Peashooter.projectile(beetle.center_x, beetle.center_y, angle, beetle)
            self.projectiles_list.append(projectile)
            self.physics_engine.add_sprite_list(self.projectiles_list,
                                                elasticity = 0.1,
                                                collision_type = "red_pea" if beetle.team_color == TeamColor.RED else "green_pea"
                                                )
        elif self.mode == __class__.TesterMode.MOVING:
            # TODO pass in click as movement location for beetle.
            print(f"Moving {'Green' if beetle.team_color == TeamColor.GREEN else 'Red'} Beetle to {x}, {y}!")

    def on_click_mode(self, event):
        if self.mode == __class__.TesterMode.SHOOTING:
            self.mode = __class__.TesterMode.MOVING
            self.mode_button.text = "Moving"
        elif self.mode == __class__.TesterMode.MOVING:
            self.mode = __class__.TesterMode.SHOOTING
            self.mode_button.text = "Shooting"

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.green_team.on_draw()
        self.red_team.on_draw()
        self.projectiles_list.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        self.green_team.on_update(delta_time)
        self.red_team.on_update(delta_time)
        self.projectiles_list.on_update(delta_time)
        self.physics_engine.step()

    class TesterMode(Enum):
        SHOOTING = 0,
        MOVING = 1

if __name__ == "__main__":
    app = BeetleTestes()
    app.setup()
    arcade.run()