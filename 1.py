import arcade
import random
import math

from pyglet.event import EVENT_HANDLE_STATE
from pyglet.graphics import Batch

from arcade.key import SPACE

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = "mario"
RESULT_COIN = 0
SPEED = 10

class Mario(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Загрузка текстур для анимации ходьбы
        self.mario = arcade.load_texture("images/mario/mario.png", hit_box_algorithm=arcade.hitbox.algo_detailed)
        # self.mario = [arcade.load_texture("images/mario/mario.png", hit_box_algorithm=arcade.hitbox.algo_detailed), arcade.load_texture("images/mario/mario_jump.png", hit_box_algorithm=arcade.hitbox.algo_detailed)]
        # self.mario[0].width = 50
        # self.mario[0].height = 50
        # self.mario[1].width = 50
        # self.mario[1].height = 50
        self.mario.width = 50
        self.mario.height = 50
        self.animation_timer = 0
        self.current_texture = 0

    def update(self, delta_time):
        # # Ограничение движения в пределах экрана
        # if self.left < 0:
        #     self.left = 0
        # if self.right > SCREEN_WIDTH:
        #     self.right = SCREEN_WIDTH
        # if self.bottom < 0:
        #     self.bottom = 0
        # if self.top > SCREEN_HEIGHT:
        #     self.top = SCREEN_HEIGHT

        # Обновление позиции
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Анимация ходьбы
        # self.animation_timer += 1
        # if self.animation_timer >= 10:
        #     self.animation_timer = 0
        #     self.current_texture = 1 - self.current_texture
        #     self.texture = self.mario[self.current_texture]


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

    def setup(self):
        # Спрайты
        self.background_sprites = arcade.SpriteList()
        self.mario_sprites = arcade.SpriteList()


        self.mario = Mario()
        self.mario.center_x = SCREEN_WIDTH // 4
        self.mario.center_y = SCREEN_HEIGHT // 4.5
        # self.mario = arcade.Sprite(player)
        self.mario_sprites.append(self.mario)

        brick_texture = arcade.load_texture("images/BrickBlockBrown.png", hit_box_algorithm=arcade.hitbox.algo_detailed)
        self.brick = arcade.Sprite(brick_texture)
        self.brick.scale = 2.5
        self.brick.center_x = SCREEN_WIDTH // 2
        self.brick.center_y = SCREEN_HEIGHT // 4.5
        self.background_sprites.append(self.brick)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height))
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
        self.mario_sprites.draw()
        self.background_sprites.draw()

    def on_key_press(self, key, modifiers):
        if key == SPACE:
            print('OK')
        if key == arcade.key.LEFT:
            self.mario.change_x = -SPEED
        elif key == arcade.key.RIGHT:
            self.mario.change_x = SPEED

    def on_update(self, delta_time: float) -> bool | None:
        for obstacles in self.background_sprites:
            collision_result = arcade.check_for_collision(self.mario, obstacles)
            if collision_result:
                self.mario.change_x = 0
        self.mario_sprites.update(delta_time)

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.mario.change_y = 0
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.mario.change_x = 0


def setup_game(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title="Mario"):
    game = MarioGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
