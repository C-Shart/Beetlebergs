import arcade
import arcade.gui
from teams import Team
from team_color import TeamColor

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Welcome to the Ouch, Motherfucker"

class BeetleBattle(arcade.View):
    def __init__(self):
        super().__init__()

        self.background = None

        self.green_team = None
        self.red_team = None

        self.physics_engine = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.settings_box = arcade.gui.UIBoxLayout()

        self.start_match_button = arcade.gui.UIFlatButton(text="Start Beetle Battle!", width=200)
        self.start_match_button.on_click = self.on_click_start_match

        self.reset_button = arcade.gui.UIFlatButton(text="Reset", width = 200)
        self.reset_button.on_click = self.on_click_reset

        self.settings_box.add(self.start_match_button.with_space_around(bottom=20))
        self.settings_box.add(self.reset_button.with_space_around(bottom=20))
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="top", child=self.settings_box))

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("Assets/Images/octagon.png")
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def setup(self):
        self.start_match_button.text = "Start Beetle Battle!"

        self.green_team = Team(TeamColor.GREEN, 320, 260)
        self.green_team.set_up_team()

        self.red_team = Team(TeamColor.RED, 960, 260)
        self.red_team.set_up_team()

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
                beetle.damage(pea.power)
                print(f"{'Green' if beetle.team.color == TeamColor.GREEN else 'Red'} Beetle hit! Current HP is {beetle.hit_points}!")
                return False # Yes, we hit but we don't want the beetle to go flying off, so we return False
            else:
                return False

        self.physics_engine.add_collision_handler("pea", "beetle", pea_handler)

    def on_click_start_match(self, event):
        self.green_team.active = not self.green_team.active
        self.red_team.active = not self.red_team.active
        if self.green_team.active:
            self.start_match_button.text = "Stop the Beetle Battle!"
        else:
            self.start_match_button.text = "Start Beetle Battle!"

    def on_click_reset(self, _event):
        self.setup()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.green_team.on_draw()
        self.red_team.on_draw()
        self.manager.draw()

    def on_update(self, delta_time):
        self.green_team.on_update(delta_time)
        self.red_team.on_update(delta_time)
        self.physics_engine.step()
        self.physics_engine.resync_sprites()

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    battle_view = BeetleBattle()
    window.show_view(battle_view)
    battle_view.setup()
    arcade.run()