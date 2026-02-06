import arcade
from PIL.ImageOps import scale
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Mario"
SPEED = 2


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Загрузка текстур для анимации ходьбы
        self.mario = [arcade.load_texture("images/mario/mario.png"), arcade.load_texture("images/mario/mario.png")]
        self.mario[0].width = 35
        self.mario[0].height = 35
        self.mario[1].width = 35
        self.mario[1].height = 35
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


class MyGUIWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout(y=self.height // 3)  # Центрирует виджеты
        self.box_layout_v = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек
        self.box_layout_h = UIBoxLayout(vertical=False, space_between=10)


        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже

        self.box_layout_v.add(self.box_layout_h)
        self.anchor_layout.add(self.box_layout_v)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

        self.all_sprites = arcade.SpriteList()

    def setup_widgets(self):
        # Здесь добавим ВСЕ виджеты — по порядку!
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")
        texture_button = UITextureButton(text='Pink Worm',
                                         texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=1.0)
        texture_button.on_click = self.change_hero
        self.box_layout_v.add(texture_button)

        texture_button1 = UITextureButton(text='Green Worm',
                                          texture=texture_normal,
                                          texture_hovered=texture_hovered,
                                          texture_pressed=texture_pressed,
                                          scale=1.0)
        texture_button1.on_click = self.change_hero1
        self.box_layout_v.add(texture_button1)

        texture_button2 = UITextureButton(text='Frog',
                                          texture=texture_normal,
                                          texture_hovered=texture_hovered,
                                          texture_pressed=texture_pressed,
                                          scale=1.0)
        texture_button2.on_click = self.change_hero2
        self.box_layout_v.add(texture_button2)

        texture_button3 = UITextureButton(text='Mario',
                                          texture=texture_normal,
                                          texture_hovered=texture_hovered,
                                          texture_pressed=texture_pressed,
                                          scale=1.0)
        texture_button3.on_click = self.change_hero3
        self.box_layout_v.add(texture_button3)

    def setup(self):
        self.texture = arcade.load_texture(f"images/background.jpg")
        self.player = Player()
        self.player.center_x = SCREEN_WIDTH // 6.5
        self.player.center_y = SCREEN_HEIGHT // 6.5
        self.all_sprites.append(self.player)

    def change_hero(self, event):
        self.player.hero = 0

    def change_hero1(self, event):
        self.player.hero = 1

    def change_hero2(self, event):
        self.player.hero = 2

    def change_hero3(self, event):
        self.player.hero = 3

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height))
        self.manager.draw()  # Рисуй GUI поверх всего
        self.all_sprites.draw()

    def on_update(self, delta_time: float) -> bool | None:
        self.all_sprites.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = SPEED

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.UP, arcade.key.DOWN]:
            self.player.change_y = 0
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0


def setup_game(width=800, height=600, title="Mario"):
    game = MyGUIWindow(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()