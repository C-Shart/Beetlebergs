import arcade
import arcade.gui
from beetles import Beetle
from spatial_manager import SpatialManager
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
        self.predicted_team = None
        self.player_keeps_playing = True

        self.physics_engine = None

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.ui_box = arcade.gui.UIBoxLayout()

        self.betting_prompt_label = None
        self.result_judgement_label = None
        self.bet_green_button = None
        self.bet_red_button = None

        self.match_over_prompt_label = None
        self.match_over_confirm_button = None

        arcade.load_font("Assets/Fonts/LuckiestGuy-Regular.ttf")
        self.buttons_style = {"font_name": "Luckiest Guy"}

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center", anchor_y="center", child=self.ui_box))

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("Assets/Images/octagon.png")
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_hide_view(self):
        # Doing this because otherwise it's possible to get into a weird state where the confirm button still accepts
        # input on the TitleView
        self.ui_box.clear()

    def setup(self):
        BEETLES_PER_TEAM = 10
        self.green_team = Team(TeamColor.GREEN, 605, 275)
        for _ in range(BEETLES_PER_TEAM - 1):
            self.green_team.beetles.append(Beetle(self.green_team))
        self.green_team.set_up_team()

        self.red_team = Team(TeamColor.RED, 705, 275)
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

        self.spatial_manager = SpatialManager()
        self.spatial_manager.add_sprite_list(self.green_team.beetles)
        self.spatial_manager.add_sprite_list(self.red_team.beetles)

        self.ui_box.clear()

        self.betting_prompt_label = arcade.gui.UILabel(
            text="Which Team will REIGN SUPREME? Make your bet!",
            font_name="Luckiest Guy",
            font_size=36,
            text_color=arcade.color.BURNT_ORANGE)
        self.betting_prompt_label.fit_content()
        self.ui_box.add(self.betting_prompt_label.with_space_around(bottom=20))

        betting_buttons_style = {"font_name": "Luckiest Guy"}
        self.bet_green_button = arcade.gui.UIFlatButton(text="Bet on Green", width=200, style=betting_buttons_style)
        self.bet_red_button = arcade.gui.UIFlatButton(text="Bet on Red", width=200, style=betting_buttons_style)
        self.bet_green_button.on_click = self.on_click_bet_green
        self.bet_red_button.on_click = self.on_click_bet_red
        self.ui_box.add(self.bet_green_button.with_space_around(bottom=20))
        self.ui_box.add(self.bet_red_button.with_space_around(bottom=20))

    def on_click_bet_green(self, event):
        self.on_click_bet(event, TeamColor.GREEN)

    def on_click_bet_red(self, event):
        self.on_click_bet(event, TeamColor.RED)

    def on_click_bet(self, event, team_color):
        self.predicted_team = team_color
        # TODO: Have a count-down
        self.ui_box.clear()
        self.green_team.active = True
        self.red_team.active = True

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.green_team.on_draw()
        self.red_team.on_draw()
        self.manager.draw()

    def on_update(self, delta_time):
        self.spatial_manager.on_update(delta_time)
        self.green_team.on_update(delta_time)
        self.red_team.on_update(delta_time)
        self.physics_engine.step()
        self.physics_engine.resync_sprites()

        if self.predicted_team:
            green_team_is_alive = False
            for beetle in self.green_team.beetles:
                if beetle.hit_points > 0:
                    green_team_is_alive = True
                    break
            red_team_is_alive = False
            for beetle in self.red_team.beetles:
                if beetle.hit_points > 0:
                    red_team_is_alive = True
                    break

            if green_team_is_alive and not red_team_is_alive:
                self.pick_winner(TeamColor.GREEN)
            elif not green_team_is_alive and red_team_is_alive:
                self.pick_winner(TeamColor.RED)
            elif not green_team_is_alive and not red_team_is_alive:
                self.pick_winner(TeamColor.NEUTRAL)

    def pick_winner(self, winning_color):
        self.green_team.active = False
        self.red_team.active = False

        prompt_text = "BATTLE OVER! "
        if winning_color == TeamColor.GREEN:
            prompt_text += "Green gets the glory!"
        elif winning_color == TeamColor.RED:
            prompt_text += "Red relishes a rout!"
        elif winning_color == TeamColor.NEUTRAL:
            prompt_text += "It's a tie! Nobody wins..."

        self.match_over_prompt_label = arcade.gui.UILabel(
            text=prompt_text,
            font_name="Luckiest Guy",
            font_size=36,
            text_color=arcade.color.BURNT_ORANGE)
        self.match_over_prompt_label.fit_content()
        self.ui_box.add(self.match_over_prompt_label.with_space_around(bottom=20))

        predicted_team = self.predicted_team
        self.predicted_team = None # to keep the update code above from running

        judgement_text = ""
        if predicted_team == winning_color:
            judgement_text = "Good betting! But can you keep it up?"
            self.player_keeps_playing = True
        elif winning_color == TeamColor.NEUTRAL:
            judgement_text = "Draw means House wins! Sorry, friend. Better luck next time!"
            self.player_keeps_playing = False
        else:
            judgement_text = "Too bad! Better luck betting next time!"
            self.player_keeps_playing = False

        self.result_judgement_label = arcade.gui.UILabel(
            text=judgement_text,
            font_name="Luckiest Guy",
            font_size=18,
            text_color=arcade.color.SLATE_BLUE)
        self.result_judgement_label.fit_content()
        self.ui_box.add(self.result_judgement_label.with_space_around(bottom=20))

        confirm_text = "Right on!" if self.player_keeps_playing else "That's that."
        self.match_over_confirm_button = arcade.gui.UIFlatButton(text=confirm_text, width=200, style=self.buttons_style)
        self.match_over_confirm_button.on_click = self.on_click_confirm_match_over
        self.ui_box.add(self.match_over_confirm_button.with_space_around(bottom=20))

    def on_click_confirm_match_over(self, event):
        if self.player_keeps_playing:
            self.setup()
        else:
            # import down here to avoid circular import
            from title_view import TitleView

            title_view = TitleView()
            self.window.show_view(title_view)

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    battle_view = BeetleBattle()
    window.show_view(battle_view)
    battle_view.setup()
    arcade.run()