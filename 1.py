import arcade
import random
import math

from arcade.key import SPACE

# Константы
SCREEN_WIDTH = 1641
SCREEN_HEIGHT = 601
SCREEN_TITLE = "mario"
RESULT_COIN = 0
SPEED = 10

class Mario(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Загрузка текстур для анимации ходьбы
        self.mario = [arcade.load_texture("images/mario/mario.png"), arcade.load_texture("images/mario/mario.png")]
        self.mario[0].width = 50
        self.mario[0].height = 50
        self.mario[1].width = 50
        self.mario[1].height = 50
        self.animation_timer = 0
        self.current_texture = 0

    def update(self, delta_time):
        # Обновление позиции
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Анимация ходьбы
        self.animation_timer += 1
        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.current_texture = 1 - self.current_texture
            self.texture = self.mario[self.current_texture]


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
        self.mario.width = 25
        self.mario.height = 25

        self.all_sprites = arcade.SpriteList()

    def setup(self):
        self.player = Mario()
        self.player.center_x = SCREEN_WIDTH // 4
        self.player.center_y = SCREEN_HEIGHT // 4.5
        self.all_sprites.append(self.player)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height))
        # arcade.draw_texture_rect(self.mario, arcade.rect.XYWH(
        #     self.width // 4, self.height // 6, 50, 50))
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
        self.all_sprites.draw()

    def on_key_press(self, key, modifiers):
        if key == SPACE:
            print('OK')
        if key == arcade.key.LEFT:
            self.player.change_x = -SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = SPEED

    def on_update(self, delta_time: float) -> bool | None:
        self.all_sprites.update()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.player.change_y = 0
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0


def setup_game(width=1200, height=800, title="Mario"):
    game = MarioGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
