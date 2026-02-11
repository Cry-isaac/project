import arcade
import random
import math
from arcade.gui import UIManager, UITextureButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

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

        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout(y=self.height / 10000)  # Центрирует виджеты
        self.box_layout_v = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек
        self.box_layout_h = UIBoxLayout(vertical=False, space_between=10)

        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже

        self.box_layout_v.add(self.box_layout_h)
        self.anchor_layout.add(self.box_layout_v)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager

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

    def setup_widgets(self):
        # Здесь добавим ВСЕ виджеты — по порядку!
        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")
        texture_button = UITextureButton(text='Level 1',
                                         texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         scale=1.0)
        texture_button.on_click = self.level1
        self.box_layout_v.add(texture_button)

        texture_button1 = UITextureButton(text='Level 2',
                                          texture=texture_normal,
                                          texture_hovered=texture_hovered,
                                          texture_pressed=texture_pressed,
                                          scale=1.0)
        texture_button1.on_click = self.level2
        self.box_layout_v.add(texture_button1)

        texture_button2 = UITextureButton(text='Level 3',
                                          texture=texture_normal,
                                          texture_hovered=texture_hovered,
                                          texture_pressed=texture_pressed,
                                          scale=1.0)
        texture_button2.on_click = self.level3
        self.box_layout_v.add(texture_button2)

        texture_button3 = UITextureButton(text='Level 4',
                                          texture=texture_normal,
                                          texture_hovered=texture_hovered,
                                          texture_pressed=texture_pressed,
                                          scale=1.0)
        texture_button3.on_click = self.level4
        self.box_layout_v.add(texture_button3)

    def level1(self):
        pass

    def level2(self):
        pass

    def level3(self):
        pass

    def level4(self):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height))
        arcade.draw_texture_rect(self.mario, arcade.rect.XYWH(
            self.width // 4, self.height // 6, 50, 50))
        arcade.draw_text('Mario', self.width // 10 * 3.3, self.height // 3 * 2, arcade.color.WHITE, 84,
                         font_name=self.custom_font)
        # arcade.draw_text('Чтобы продолжить, нажмите пробел', self.width // 10 * 2.5, self.height // 2 , arcade.color.WHITE, 12,
        #                  font_name=self.custom_font1)
        arcade.draw_text('Лучший счёт', self.width // 6, self.height - 20, arcade.color.WHITE, 12,
                         font_name=self.custom_font1)
        arcade.draw_text("0000", self.width // 6, self.height - 40, arcade.color.WHITE, 12,
                         font_name=self.custom_font1)
        self.manager.draw()  # Рисуй GUI поверх всего

    def on_key_press(self, key, modifiers):
        pass


def setup_game(width=1200, height=800, title="Mario"):
    game = MarioGame(width, height, title)
    return game


def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
