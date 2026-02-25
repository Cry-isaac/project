import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Mario-style Game"


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.wall_list = None
        self.player = None
        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0

    def setup(self):
        map_name = "безымянный.tmx"
        my_map = arcade.tilemap.load_tilemap(map_name)

        self.scene = arcade.Scene.from_tilemap(my_map)

        self.wall_list = self.scene.get_sprite_list("Walls")
        self.coin_list = self.scene.get_sprite_list("Coins")
        self.background_list = self.scene.get_sprite_list("Background")

        self.player = arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png",
                                    0.5)
        self.player.center_x = 128
        self.player.center_y = 128

        self.scene.add_sprite("Player", self.player)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list, gravity_constant=0.5)

    def on_update(self, delta_time):
        self.physics_engine.update()
        changed = False

        left_boundary = self.view_left + SCREEN_WIDTH - SCREEN_WIDTH / 3
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH / 3
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - SCREEN_HEIGHT / 3
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + SCREEN_HEIGHT / 3
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_draw(self):
        self.clear()
        self.wall_list.draw()
        self.player.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.physics_engine.can_jump():
            self.player.change_y = 10
        elif key == arcade.key.LEFT:
            self.player.change_x = -5
        elif key == arcade.key.RIGHT:
            self.player.change_x = 5

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.player.change_x = 0


def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()