import arcade
import random
import math

# Константы
SCREEN_WIDTH = 1641
SCREEN_HEIGHT = 601
SCREEN_TITLE = "mario"
RESULT_COIN = 0


class MarioGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        arcade.set_background_color(arcade.color.BLACK)
        arcade.load_font('fonts/tlpsmb.ttf')
        arcade.load_font('fonts/VMVSegaGenesis-Regular.otf')
        self.custom_font = 'Super Mario Brothers'
        self.custom_font1 = 'VMV Sega Genesis'

    def on_draw(self):
        self.clear()
        arcade.draw_text('Mario', self.width // 10 * 3, self.height // 3 * 2, arcade.color.WHITE, 84,
                         font_name=self.custom_font)
        arcade.draw_text('Чтобы продолжить, нажмите пробел', self.width // 10 * 2.5, self.height // 2 , arcade.color.WHITE, 12,
                         font_name=self.custom_font1)
        arcade.draw_text('Лучший счёт', self.width // 6, self.height - 20, arcade.color.WHITE, 12,
                         font_name=self.custom_font1)
        arcade.draw_text("0000", self.width // 6, self.height - 40, arcade.color.WHITE, 12,
                         font_name=self.custom_font1)

    def on_key_press(self, key, modifiers):
        pass


def setup_game(width=1000, height=600, title="Catching fish"):
    game = MarioGame(width, height, title)
    return game


def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
