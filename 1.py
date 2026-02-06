import arcade
import random
import math

from arcade.key import SPACE

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

        # Шрифты
        arcade.load_font('fonts/tlpsmb.ttf')
        arcade.load_font('fonts/VMVSegaGenesis-Regular.otf')
        self.custom_font = 'Super Mario Brothers'
        self.custom_font1 = 'VMV Sega Genesis'

        # Фон меню
        self.background = arcade.load_texture(f"images/background.jpg")

        # Текстура Марио
        self.mario = arcade.load_texture("images/mario/mario.png")
        self.mario.width = 100
        self.mario.height = 100

    def setup(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height))
        arcade.draw_texture_rect(self.mario, arcade.rect.XYWH(
            self.width // 4, self.height // 6, 50, 50))
        arcade.draw_text('Mario', self.width // 10 * 3, self.height // 3 * 2, arcade.color.WHITE, 84,
                         font_name=self.custom_font)
        arcade.draw_text('Чтобы продолжить, нажмите пробел', self.width // 10 * 2.5, self.height // 2 , arcade.color.WHITE, 12,
                         font_name=self.custom_font1)
        arcade.draw_text('Лучший счёт', self.width // 6, self.height - 20, arcade.color.WHITE, 12,
                         font_name=self.custom_font1)
        arcade.draw_text("0000", self.width // 6, self.height - 40, arcade.color.WHITE, 12,
                         font_name=self.custom_font1)
        arcade.draw_text('Последний уровень', self.width // 2, self.height - 20, arcade.color.WHITE, 12,
                         font_name=self.custom_font1)
        arcade.draw_text('0-1', self.width // 2, self.height - 40, arcade.color.WHITE, 12,
                         font_name=self.custom_font1)

    def on_key_press(self, key, modifiers):
        if key == SPACE:
            print('OK')


def setup_game(width=1200, height=800, title="Mario"):
    game = MarioGame(width, height, title)
    return game


def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
