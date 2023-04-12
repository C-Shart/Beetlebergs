import arcade
from beetle_battle import BeetleBattle

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Legally-Distinct Beetlebergs!"

class TitleView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("Assets/Images/beetles.png")
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text(
            "Legally-Distinct Beetlebergs!!!", self.window.width / 2, self.window.height / 2, arcade.color.WHITE,
            font_size=50, anchor_x="center")
        arcade.draw_text(
            "Click to advance", self.window.width / 2, self.window.height / 2-75, arcade.color.WHITE, font_size=20,
            anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifies):
        battle_view = BeetleBattle()
        battle_view.setup()
        self.window.show_view(battle_view)

if __name__ == "__main__":
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    title_view = TitleView()
    window.show_view(title_view)
    arcade.run()