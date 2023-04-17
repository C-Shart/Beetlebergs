import arcade
import arcade.gui
from beetles import Beetle
from spatial_manager import SpatialManager
from teams import Team
from team_color import TeamColor

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Little Versions of Sisyphus with Carapaces"

class BeetleBattle(arcade.View):
    def __init__(self):
        super().__init__()

        self.background = None

        self.green_team = None
        self.red_team = None

        self.physics_engine = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.load_font("Assets/Fonts/LuckiestGuy-Regular.ttf")
        self.buttons_style = {"font_name": "Luckiest Guy"}

        self.ui_bg_texture = arcade.load_texture(":resources:gui_basic_assets/window/grey_panel.png")

        self.settings_box = arcade.gui.UIBoxLayout()

        self.battles_to_run = 5
        self.battle_count_box = arcade.gui.UIBoxLayout(vertical=False)
        self.battle_count_label = None
        self.battle_count_text = None

        self.status_text_label = arcade.gui.UILabel(font_size=24, text_color=arcade.color.RED)

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="left", anchor_y="top", child=self.settings_box))
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center", anchor_y="bottom", child=self.status_text_label))
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("Assets/Images/octagon.png")
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def setup(self):
        BEETLES_PER_TEAM = 10
        self.green_team = Team(TeamColor.GREEN, 605, 350)
        for _ in range(BEETLES_PER_TEAM - 1):
            self.green_team.beetles.append(Beetle(self.green_team))
        self.green_team.set_up_team()

        self.red_team = Team(TeamColor.RED, 705, 350)
        for _ in range(BEETLES_PER_TEAM - 1):
            self.red_team.beetles.append(Beetle(self.red_team))
        self.red_team.set_up_team()

        self.green_team.other_team = self.red_team
        self.red_team.other_team = self.green_team

        # DEBUG: Lowering the beetle's HP so this doesn't take forever
        for beetle in self.green_team.beetles:
            beetle.hit_points = 13
        for beetle in self.red_team.beetles:
            beetle.hit_points = 13

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

        self.battle_count_label = arcade.gui.UILabel(text="Battles to Run for (Blank for Indefinitely)")
        self.battle_count_label.fit_content()
        self.battle_count_text = arcade.gui.UIInputText(text="5", width=50, height=25)
        self.battle_count_box.add(self.battle_count_label)
        self.battle_count_box.add(
            arcade.gui.UITexturePane(
                self.battle_count_text,
                tex=self.ui_bg_texture,
                padding=(10, 10, 10, 10),
            )
        )
        self.settings_box.add(self.battle_count_box.with_space_around(bottom=20))

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.green_team.on_draw()
        self.red_team.on_draw()
        # self.wall_list.draw() # Not drawn by default but could be useful to see for debugging
        self.manager.draw()

    def on_update(self, delta_time):
        try:
            desired_battle_text = self.battle_count_text.text
            if desired_battle_text == "" or desired_battle_text.isspace():
                self.status_text_label.text = ""
                if self.battles_to_run != -1:
                    self.battles_to_run = -1 # To represent indefinitely
                    print("Set battles to run indefinitely")
            else:
                desired_battle_int = int(desired_battle_text)
                if desired_battle_int < 1:
                    raise ValueError("Must be at least one battle")
                self.status_text_label.text = ""
                if self.battles_to_run != desired_battle_int:
                    self.battles_to_run = desired_battle_int
                    print(f"Set battles to run to {self.battles_to_run}")
        except ValueError:
            self.status_text_label.text = "Invalid number of battles requested; must be an integer of at least 1"
            self.status_text_label.fit_content()

        self.spatial_manager.on_update(delta_time)
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