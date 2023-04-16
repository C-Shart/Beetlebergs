import arcade
import arcade.gui
import attacks
from enum import Enum
import math
from spatial_manager import SpatialManager
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

        self.green_team = None
        self.red_team = None

        self.physics_engine = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.settings_box = arcade.gui.UIBoxLayout()

        self.mode = __class__.TesterMode.SHOOTING
        self.mode_button = arcade.gui.UIFlatButton(text="Shooting", width=200)
        self.mode_button.on_click = self.on_click_mode

        self.green_auto_button = arcade.gui.UIFlatButton(text="Make Green Autonomous", width = 200)
        self.red_auto_button = arcade.gui.UIFlatButton(text="Make Red Autonomous", width = 200)
        self.green_auto_button.on_click = self.on_click_auto_green
        self.red_auto_button.on_click = self.on_click_auto_red

        self.reset_button = arcade.gui.UIFlatButton(text="Reset", width = 200)
        self.reset_button.on_click = self.on_click_reset

        self.settings_box.add(self.mode_button.with_space_around(bottom=20))
        self.settings_box.add(self.green_auto_button.with_space_around(bottom=20))
        self.settings_box.add(self.red_auto_button.with_space_around(bottom=20))
        self.settings_box.add(self.reset_button.with_space_around(bottom=20))
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="top", child=self.settings_box))

    def setup(self):
        self.background = arcade.load_texture("Assets/Images/rose_arena.png")

        self.green_team = Team(TeamColor.GREEN, 320, 260)
        self.green_team.set_up_team()
        self.green_auto_button.text = "Make Green Autonomous"

        self.red_team = Team(TeamColor.RED, 960, 260)
        self.red_team.set_up_team()
        self.red_auto_button.text = "Make Red Autonomous"

        self.green_team.other_team = self.red_team
        self.red_team.other_team = self.green_team

        self.physics_engine = arcade.PymunkPhysicsEngine()

        self.physics_engine.add_sprite_list(self.green_team.beetles,
                                            mass = 1,
                                            elasticity = 0.0,
                                            friction = 0.8,
                                            moment_of_intertia = 1,
                                            damping = 1.0,
                                            collision_type="beetle"
                                            )
        self.physics_engine.add_sprite_list(self.red_team.beetles,
                                            mass = 1,
                                            elasticity = 0.0,
                                            friction = 0.8,
                                            moment_of_intertia = 1,
                                            damping = 1.0,
                                            collision_type="beetle"
                                            )

        def pea_handler(pea, beetle, _arbiter, _space, _data):
            if pea and beetle:
                if pea.team_color == beetle.team.color:
                    return False
                pea.remove_from_sprite_lists()
                pea.spatial_manager.remove(pea)
                beetle.damage(pea.power)
                print(f"{'Green' if beetle.team.color == TeamColor.GREEN else 'Red'} Beetle hit! Current HP is {beetle.hit_points}!")
                return False # Yes, we hit but we don't want the beetle to go flying off, so we return False
            else:
                return False

        self.physics_engine.add_collision_handler("pea", "beetle", pea_handler)

        WALL_WIDTH = 500
        WALL_OFFSET = 100
        left_wall = arcade.SpriteSolidColor(WALL_WIDTH, SCREEN_HEIGHT, arcade.color.CYAN)
        left_wall.center_x = -WALL_WIDTH / 2 + WALL_OFFSET
        left_wall.center_y = SCREEN_HEIGHT / 2
        right_wall = arcade.SpriteSolidColor(WALL_WIDTH, SCREEN_HEIGHT, arcade.color.CYAN)
        right_wall.center_x = SCREEN_WIDTH + WALL_WIDTH / 2 - WALL_OFFSET
        right_wall.center_y = SCREEN_HEIGHT / 2
        bottom_wall = arcade.SpriteSolidColor(SCREEN_WIDTH, WALL_WIDTH, arcade.color.CYAN)
        bottom_wall.center_x = SCREEN_WIDTH / 2
        bottom_wall.center_y = -WALL_WIDTH / 2 + WALL_OFFSET
        top_wall = arcade.SpriteSolidColor(SCREEN_WIDTH, WALL_WIDTH, arcade.color.CYAN)
        top_wall.center_x = SCREEN_WIDTH / 2
        top_wall.center_y = SCREEN_HEIGHT + WALL_WIDTH / 2 - WALL_OFFSET
        self.wall_list = arcade.SpriteList()
        self.wall_list.append(left_wall)
        self.wall_list.append(right_wall)
        self.wall_list.append(bottom_wall)
        self.wall_list.append(top_wall)
        self.physics_engine.add_sprite_list(
            self.wall_list,
            collision_type="wall",
            body_type=arcade.PymunkPhysicsEngine.STATIC)

        def wall_handler(_pea, _wall, _arbiter, _space, _data):
            return False
        self.physics_engine.add_collision_handler("pea", "wall", wall_handler)

        self.spatial_manager = SpatialManager()
        self.spatial_manager.add_sprite_list(self.green_team.beetles)
        self.spatial_manager.add_sprite_list(self.red_team.beetles)

    def on_mouse_press(self, x, y, button, modifiers):
        beetle = self.green_team.beetles[0] if button == arcade.MOUSE_BUTTON_LEFT else self.red_team.beetles[0]
        x_distance = x - beetle.center_x
        y_distance = y - beetle.center_y
        angle = (math.degrees(math.atan2(y_distance, x_distance)))
        if self.mode == __class__.TesterMode.SHOOTING:
            peashooter_ability = beetle.abilities[0]
            peashooter_ability.active = not peashooter_ability.active
            beetle.firing_target = (x, y) if peashooter_ability.active else None
            # TODO: Turning on the peashooter like this doesn't stick because the beetle is never made active. Fix this.

        elif self.mode == __class__.TesterMode.MOVING:
            if modifiers & arcade.key.MOD_SHIFT:
                beetle.set_facing(x, y)
                print(f"Turning {'Green' if beetle.team.color == TeamColor.GREEN else 'Red'} Beetle towards {x}, {y}!")
            else:
                beetle.move_to(x, y)
                print(f"Moving {'Green' if beetle.team.color == TeamColor.GREEN else 'Red'} Beetle to {x}, {y}!")

    def on_click_mode(self, event):
        if self.mode == __class__.TesterMode.SHOOTING:
            self.mode = __class__.TesterMode.MOVING
            self.mode_button.text = "Moving"
        elif self.mode == __class__.TesterMode.MOVING:
            self.mode = __class__.TesterMode.SHOOTING
            self.mode_button.text = "Shooting"

    def on_click_auto_red(self, event):
        self.on_click_auto(event, TeamColor.RED)

    def on_click_auto_green(self, event):
        self.on_click_auto(event, TeamColor.GREEN)

    def on_click_auto(self, event, team_color):
        team = self.green_team if team_color == TeamColor.GREEN else self.red_team
        button = self.green_auto_button if team_color == TeamColor.GREEN else self.red_auto_button
        team_name = "Green" if team_color == TeamColor.GREEN else "Red"
        team.active = not team.active
        if team.active:
            button.text = f"{team_name.upper()} TEAM AUTO ON"
        else:
            button.text = f"Make {team_name} Autonomous"

    def on_click_reset(self, _event):
        self.setup()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.green_team.on_draw()
        self.red_team.on_draw()
        # self.wall_list.draw() # Not drawn by default but could be useful to see for debugging
        self.manager.draw()

    def on_update(self, delta_time):
        self.spatial_manager.on_update(delta_time)
        self.green_team.on_update(delta_time)
        self.red_team.on_update(delta_time)
        self.physics_engine.step()
        self.physics_engine.resync_sprites()

    class TesterMode(Enum):
        SHOOTING = 0,
        MOVING = 1

if __name__ == "__main__":
    app = BeetleTestes()
    app.setup()
    arcade.run()