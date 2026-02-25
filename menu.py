import arcade
import random
import enum
from arcade import Text
import pytmx

# Константы
MAP_SCALING = 1.0
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "menu"
RESULT_COIN = 0
ANIMATION_SPEED = 0.1
GRAVITY = 1.0
PLAYER_START_X = 65
PLAYER_START_Y = 256


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1


class Mario(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # Загружаем текстуры для анимации
        self.textures = []
        self.textures.append(arcade.load_texture(f"images/run1.png"))
        self.textures.append(arcade.load_texture(f"images/to_stand.png"))
        self.textures.append(arcade.load_texture(f"images/run2.png"))
        self.textures.append(arcade.load_texture(f"images/run3.png"))

        self.texture = self.textures[1]
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = 120
        self.scale = 0.5
        self.speed = 100
        self.is_walking = False
        self.face_direction = FaceDirection.RIGHT
        self.timer = 0
        self.current_picture = 1
        self.is_jumping = False
        self.gravity = -300
        self.jump_speed = 0
        self.posit = self.center_y
        self.jump_texture = arcade.load_texture(f"images/jump.png")
        self.fall_texture = arcade.load_texture(f"images/fall.png")
        self.is_falling_back = False
        self.fall_speed = 100
        self.start_x = self.center_x
        self.start_y = self.center_y
        self.screen_title = SCREEN_TITLE

    def update(self, delta_time, keys_pressed):
        if self.is_falling_back:
            self.center_y -= self.fall_speed * delta_time
            if self.bottom <= 0:
                self.bottom = 0
                self.is_falling_back = False
                self.center_x = self.start_x
                self.center_y = self.start_y
            return
        self.is_walking = False
        if arcade.key.RIGHT in keys_pressed:
            self.face_direction = FaceDirection.RIGHT
            self.center_x += self.speed * delta_time
            self.is_walking = True
        if arcade.key.LEFT in keys_pressed:
            self.face_direction = FaceDirection.LEFT
            self.center_x -= self.speed * delta_time
            self.is_walking = True

        if self.is_jumping:
            self.center_y += self.jump_speed * delta_time
            self.jump_speed += self.gravity * delta_time
            # условие приземления
            if self.center_y <= self.posit:
                self.center_y = self.posit
                self.is_jumping = False
                self.jump_speed = 0

        if self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.left < 0:
            self.left = 0
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.bottom < 0:
            self.bottom = 0

    def update_animation(self, delta_time: float = 1 / 60):
        if self.is_jumping:
            self.texture = self.jump_texture
            new_texture = self.texture
            self.texture = new_texture.flip_horizontally() if self.face_direction == FaceDirection.LEFT else new_texture
        elif self.is_walking:
            self.timer += delta_time
            if self.timer >= ANIMATION_SPEED:
                self.timer = 0
                self.current_picture = (self.current_picture + 1) % len(self.textures)
            new_texture = self.textures[self.current_picture]
            self.texture = new_texture.flip_horizontally() if self.face_direction == FaceDirection.LEFT else new_texture
        else:
            self.texture = self.textures[1]

        if self.is_falling_back:
            self.texture = self.fall_texture


class Coin(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("mario_comb/images/score.png")
        self.center_x = x
        self.center_y = y
        self.scale = 0.04
        self.coin_speed = random.uniform(100, 200)


class Mushroom(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.textures_mushroom_to_stand = arcade.load_texture(f"images/mushroom.png")
        self.textures_mushroom_compressed = arcade.load_texture(f"images/mushroom_compressed.png")
        self.current_texture_index = 0
        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = 115
        self.scale = 0.07
        self.mushroom_speed = random.randint(100, 200)
        self.mushroom_compressed_flag = False
        self.compressed = False
        self.mushroom_timer = 0
        self.remove_flag = False

    def update(self, delta_time):
        if self.mushroom_compressed_flag:
            self.center_y -= 100 * delta_time
            if self.bottom <= -100:
                self.bottom = -100
                self.mushroom_compressed_flag = False
            return
        self.center_x += self.mushroom_speed * delta_time
        if self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            self.mushroom_speed *= -1
        elif self.left <= 0:
            self.left = 0
            self.mushroom_speed *= -1

    def update_animation(self, delta_time):
        if self.mushroom_compressed_flag:
            self.texture = self.textures_mushroom_compressed
            self.remove_flag = True
        else:
            self.texture = self.textures_mushroom_to_stand
            self.mushroom_timer += delta_time
            if self.mushroom_timer <= 0.3:
                self.mushroom_compressed_flag = False
                self.mushroom_timer = 0
                self.texture = self.textures_mushroom_to_stand


class Turtle(arcade.Sprite):
    def __init__(self):
        super().__init__()
        # Загружаем текстуры
        self.texture_normal = arcade.load_texture("images/turtle.png")
        self.texture_shell = arcade.load_texture("images/shell.png")
        self.texture = self.texture_normal

        # Позиция и размер
        self.center_x = -50  # Появляется слева
        self.center_y = 115
        self.scale = 0.23

        # Скорость и состояние
        self.speed = random.randint(150, 250)
        self.is_shell = False
        self.shell_timer = 0
        self.shell_speed = 0
        self.shell_moving = False
        self.can_be_kicked = True
        self.kick_cooldown = 0  # Кулдаун между ударами
        self.stun_timer = 0  # Таймер оглушения

        self.face_direction = FaceDirection.RIGHT

    def update(self, delta_time):
        # Обновляем таймеры
        if self.kick_cooldown > 0:
            self.kick_cooldown -= delta_time
        if self.stun_timer > 0:
            self.stun_timer -= delta_time

        if self.is_shell:
            # Если панцирь движется
            if self.shell_moving:
                self.center_x += self.shell_speed * delta_time
                # Проверка границ - отскок от стен
                if self.right >= SCREEN_WIDTH:
                    self.right = SCREEN_WIDTH
                    self.shell_speed *= -1
                    self.can_be_kicked = True  # Можно снова пнуть после отскока
                    self.stun_timer = 0.2  # Небольшое оглушение после отскока
                elif self.left <= 0:
                    self.left = 0
                    self.shell_speed *= -1
                    self.can_be_kicked = True  # Можно снова пнуть после отскока
                    self.stun_timer = 0.2  # Небольшое оглушение после отскока
            return

        # Обычное движение черепахи
        x = self.center_x
        self.center_x += self.speed * delta_time

        if self.center_x > x:
            self.face_direction = FaceDirection.RIGHT
        elif self.center_x < x:
            self.face_direction = FaceDirection.LEFT

        # Проверка границ
        if self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
            self.speed *= -1
        elif self.left <= 0:
            self.left = 0
            self.speed *= -1

    def update_animation(self, delta_time):
        if self.is_shell:
            self.texture = self.texture_shell
            # Анимация вращения для движущегося панциря
            if self.shell_moving:
                self.angle += 10
        else:
            if self.face_direction == FaceDirection.LEFT:
                self.texture = self.texture_normal.flip_horizontally()
            else:
                self.texture = self.texture_normal
            self.angle = 0

        # Таймер для возврата из панциря
        if self.is_shell and not self.shell_moving and self.stun_timer <= 0:
            self.shell_timer += delta_time
            if self.shell_timer >= 3.0:  # Через 3 секунды возвращается
                self.is_shell = False
                self.shell_timer = 0
                self.texture = self.texture_normal
                self.can_be_kicked = True

    def become_shell(self):
        """Становится панцирем"""
        self.is_shell = True
        self.shell_timer = 0
        self.shell_moving = False
        self.shell_speed = 0
        self.can_be_kicked = True
        self.stun_timer = 0.5  # Короткое оглушение после превращения

    def kick_shell(self, direction):
        """Пнуть панцирь"""
        if self.is_shell and self.can_be_kicked and self.kick_cooldown <= 0:
            self.shell_moving = True
            self.shell_speed = 500 * direction  # Увеличена скорость
            self.can_be_kicked = False
            self.kick_cooldown = 0.3  # Небольшая задержка между ударами
            self.stun_timer = 0  # Сбрасываем оглушение при ударе


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.uniform(2, 4)
        self.color = arcade.color.WHITE
        self.velocity_x = random.uniform(-50, 50)
        self.velocity_y = random.uniform(50, 150)
        self.life_time = random.uniform(0.5, 1.0)
        self.frame = 0

    def update(self, delta_time):
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        self.life_time -= delta_time
        # Можно добавить затухание или изменение цвета со временем

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)


def play_music():
    music = arcade.load_sound('images/Марио_1.mp3')
    arcade.play_sound(music)


class MarioGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        self.world_camera = arcade.camera.Camera2D()
        self.ui_camera = arcade.camera.Camera2D()
        self.background = arcade.load_texture(f"images/i.png")
        self.mario = arcade.SpriteList()
        self.score_number = 0
        self.score_texture = arcade.load_texture("mario_comb/images/score.png")
        self.heart = arcade.load_texture("mario_comb/images/heart.png")
        self.score_heart_number = 4
        self.score_heart = Text("4", self.width - 75, self.height - 70, arcade.color.WHITE, 30)
        self.score_heart_menu = Text("4", self.width // 2 + 40, self.height // 2 - 90, arcade.color.WHITE, 30)
        self.score = Text("0", self.width - 75, self.height - 35, arcade.color.WHITE, 30)
        self.game_over = Text("GAME OVER", (self.width // 2) - 200, self.height // 2, arcade.color.RED, 60)
        self.press_space = Text("Press [G] to start the game again", (self.width // 2) - 300,
                                (self.height // 2) - 100, arcade.color.RED, 30)
        self.win = Text("YOU WIN", (self.width // 2) - 130, self.height // 2, arcade.color.WHITE, 60)
        self.all_coins = Text("10", (self.width // 2) + 40, self.height // 2 - 150,
                              arcade.color.WHITE, 30)
        self.coins = arcade.SpriteList()
        self.timer_coin = 0
        self.count_coin = 0
        self.mushroom = arcade.SpriteList()
        self.turtle = arcade.SpriteList()  # Список для черепах
        self.mushroom_respawns = []
        self.game_over_flag = False
        self.screen_title = SCREEN_TITLE
        self.show_mario_text = True
        self.particles = []  # список частиц
        self.win_flag = False
        self.coins_collected = 0
        self.result = False

        # Карта
        tmxdata = pytmx.TiledMap("level_1.tmx")

        # Шрифты
        arcade.load_font('fonts/tlpsmb.ttf')
        arcade.load_font('fonts/VMVSegaGenesis-Regular.otf')
        self.custom_font = 'Super Mario Brothers'
        self.custom_font1 = 'VMV Sega Genesis'

        # Текстура Марио
        self.hero = arcade.load_texture("images/mario.png")
        self.hero.width = 100
        self.hero.height = 100

        self.music_background = play_music()

    def save_result(self, result):
        with open('win_or_game_over_1.txt', 'a') as file:
            file.write(f"{result}\n")

    def spawn_mushroom(self):
        new_mushroom = Mushroom()
        self.mushroom.append(new_mushroom)

    def spawn_turtle(self):
        new_turtle = Turtle()
        self.turtle.append(new_turtle)

    def setup(self) -> None:
        self.mario.append(Mario())
        self.mushroom.append(Mushroom())
        self.turtle.append(Turtle())  # Добавляем черепаху
        self.keys_pressed = set()
        self.mario[0].start_x = self.mario[0].center_x
        self.mario[0].start_y = self.mario[0].center_y
        self.level = 1

        """Sets up the game for the current level"""

        # Get the current map based on the level
        map_name = f"level_{self.level}.tmx"

        # What are the names of the layers?
        wall_layer = "Blocks"
        coin_layer = "Coins"
        goal_layer = "Exit"
        background_layer = "Background"
        money_block_layer = "Money_blocks"

        # Load the current map
        game_map = arcade.tilemap.load_map(map_name)

        # Load the layers
        self.background = arcade.tilemap.process_layer(
            game_map, layer_name=background_layer, scaling=MAP_SCALING
        )
        self.goals = arcade.tilemap.process_layer(
            game_map, layer_name=goal_layer, scaling=MAP_SCALING
        )
        self.walls = arcade.tilemap.process_layer(
            game_map, layer_name=wall_layer, scaling=MAP_SCALING
        )
        self.ladders = arcade.tilemap.process_layer(
            game_map, layer_name=money_block_layer, scaling=MAP_SCALING
        )
        self.coins = arcade.tilemap.process_layer(
            game_map, layer_name=coin_layer, scaling=MAP_SCALING
        )

        # Set the background color
        background_color = arcade.color.FRESH_AIR
        if game_map.background_color:
            background_color = game_map.background_color
        arcade.set_background_color(background_color)

        # Create the player sprite if they're not already set up
        if not self.player:
            self.player = self.create_player_sprite()

        # Move the player sprite back to the beginning
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y
        self.player.change_x = 0
        self.player.change_y = 0

        # Load the physics engine for this map
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.walls,
            gravity_constant=GRAVITY,
            ladders=self.ladders,
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # создаем несколько частиц на месте клика
            for _ in range(20):
                self.particles.append(Particle(x, y))

    def on_draw(self):
        self.ui_camera.use()
        self.clear()
        arcade.draw_texture_rect(self.background, arcade.rect.XYWH(
            self.width // 2, self.height // 2, self.width, self.height))
        if self.show_mario_text:
            arcade.draw_text('Mario', self.width - 950, self.height // 3 * 2, arcade.color.WHITE, 150,
                             font_name=self.custom_font)
            arcade.draw_text('Чтобы продолжить, нажмите пробел', self.width // 3, self.height // 2, arcade.color.WHITE,
                             12,
                             font_name=self.custom_font1)

        self.mario.draw()
        arcade.draw_texture_rect(self.score_texture, arcade.rect.XYWH(self.width - 100, self.height - 25, 30, 30))
        arcade.draw_texture_rect(self.heart, arcade.rect.XYWH(self.width - 100, self.height - 60, 30, 30))
        self.score.text = f"{self.score_number}"
        self.score_heart.text = f"{self.score_heart_number}"
        self.score_heart.draw()
        self.score.draw()
        self.coins.draw()
        self.mushroom.draw()
        self.turtle.draw()  # Рисуем черепаху

        if self.game_over_flag:
            arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, arcade.color.BLACK)
            self.mario.draw()
            self.game_over.draw()
            self.press_space.draw()
            self.check_game_over()

        if self.win_flag:
            arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, arcade.color.BLACK)
            self.win.draw()
            self.mario.draw()
            arcade.draw_texture_rect(self.heart, arcade.rect.XYWH(self.width // 2 - 10, self.height // 2 - 80, 50, 50))
            self.score_heart_menu.text = f"{self.score_heart_number}"
            self.score_heart_menu.draw()
            arcade.draw_texture_rect(self.score_texture,
                                     arcade.rect.XYWH(self.width // 2 - 10, self.height // 2 - 140, 45, 45))
            self.all_coins.draw()
            self.check_win()
            for particle in self.particles:
                particle.draw()

    def on_key_press(self, key, modifiers):
        if self.screen_title == "menu":
            if key == arcade.key.SPACE:
                self.screen_title = 'mario'
                self.show_mario_text = False
                self.setup()
        if self.win_flag or self.game_over_flag:
            if key == arcade.key.G:
                self.game_over_flag = False
                self.win_flag = False
                self.score_number = 0
                self.score_heart_number = 4
                self.count_coin = 0
                self.spawn_mushroom()
                self.spawn_turtle()

        self.keys_pressed.add(key)
        if key == arcade.key.SPACE and not self.mario[0].is_jumping:
            self.mario[0].is_jumping = True
            self.mario[0].jump_speed = 300
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def check_game_over(self):
        if self.game_over_flag and not self.result:
            self.save_result(f'game over, score - {self.score_number}, heart - 0')
            self.result = True

    def check_win(self):
        if self.win_flag and not self.result:
            self.save_result(f'win, score - 10, heart - {self.score_heart_number}')
            self.result = True

    def on_update(self, delta_time):
        if len(self.mario) > 0:
            position = (
                self.mario[0].center_x,
                self.mario[0].center_y
            )
            self.ui_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
                self.world_camera.position,
                position,
                0.12)

        # Обновление частиц
        for particle in self.particles[:]:
            particle.update(delta_time)
            if particle.life_time <= 0:
                self.particles.remove(particle)

        # Обновление грибов
        for mushroom in self.mushroom:
            mushroom.update(delta_time)
            mushroom.update_animation(delta_time)

        # Обновление черепах
        for turtle in self.turtle:
            turtle.update(delta_time)
            turtle.update_animation(delta_time)

        # Обновление Марио
        for sprite in self.mario:
            sprite.update(delta_time, self.keys_pressed)
            sprite.update_animation(delta_time)

        # Проверка коллизий с грибами
        for turtle in self.turtle:
            for sprite in self.mario:
                for mushroom in self.mushroom[:]:
                    if arcade.check_for_collision(sprite, mushroom):
                        if sprite.center_y > mushroom.center_y + mushroom.height / 4:
                            mushroom.mushroom_compressed_flag = True
                            mushroom.mushroom_timer = 0
                            self.mushroom.update()
                            # Добавляем частицы
                            for _ in range(5):
                                self.particles.append(Particle(mushroom.center_x, mushroom.center_y))
                        else:
                            mushroom.mushroom_speed *= -1
                            sprite.is_falling_back = True
                            sprite.start_x = sprite.center_x
                            sprite.start_y = sprite.center_y
                            self.score_heart_number -= 1
                            if self.score_heart_number <= 0:
                                self.game_over_flag = True
                                self.mushroom.remove(mushroom)
                                self.turtle.remove(turtle)
                            else:
                                self.mushroom.remove(mushroom)
                                self.spawn_mushroom()

        # Проверка коллизий с черепахами
        for sprite in self.mario:
            for turtle in self.turtle[:]:
                if arcade.check_for_collision(sprite, turtle):
                    # Марио падает сверху на черепаху
                    if sprite.center_y > turtle.center_y + turtle.height / 4:
                        if turtle.is_shell:
                            # Если черепаха уже в панцире - пинаем её
                            if sprite.center_x < turtle.center_x:
                                turtle.kick_shell(1)  # Пинаем вправо
                            else:
                                turtle.kick_shell(-1)  # Пинаем влево
                            # Добавляем частицы
                            for _ in range(5):
                                self.particles.append(Particle(turtle.center_x, turtle.center_y))
                        else:
                            # Превращаем в панцирь
                            turtle.become_shell()
                            # Добавляем частицы
                            for _ in range(5):
                                self.particles.append(Particle(turtle.center_x, turtle.center_y))
                    else:
                        # Столкновение сбоку
                        if turtle.is_shell:
                            if turtle.shell_moving:
                                # Если панцирь движется и попадает в Марио
                                self.score_heart_number -= 1
                                sprite.is_falling_back = True
                                sprite.start_x = sprite.center_x
                                sprite.start_y = sprite.center_y
                                turtle.shell_speed *= -1
                                turtle.can_be_kicked = True  # Можно снова пнуть после отскока
                                turtle.stun_timer = 0.2
                                if self.score_heart_number <= 0:
                                    self.game_over_flag = True
                                    self.coins = arcade.SpriteList()
                            else:
                                # Если стоим на неподвижном панцире сбоку - пинаем его
                                if sprite.center_x < turtle.center_x:
                                    turtle.kick_shell(1)  # Пинаем вправо
                                else:
                                    turtle.kick_shell(-1)  # Пинаем влево
                                # Добавляем частицы
                                for _ in range(5):
                                    self.particles.append(Particle(turtle.center_x, turtle.center_y))
                        else:
                            # Обычная черепаха наносит урон
                            turtle.speed *= -1
                            sprite.is_falling_back = True
                            sprite.start_x = sprite.center_x
                            sprite.start_y = sprite.center_y
                            self.score_heart_number -= 1
                            if self.score_heart_number <= 0:
                                self.game_over_flag = True
                                self.coins = arcade.SpriteList()

        # Проверка столкновений черепах с грибами
        for turtle in self.turtle:
            if turtle.is_shell and turtle.shell_moving:
                for mushroom in self.mushroom[:]:
                    if arcade.check_for_collision(turtle, mushroom):
                        # Панцирь уничтожает гриб
                        self.mushroom.remove(mushroom)
                        for _ in range(10):
                            self.particles.append(Particle(mushroom.center_x, mushroom.center_y))

        # Проверка победы
        if self.score_number == 10 and self.score_heart_number > 0:
            self.win_flag = True
            self.mushroom = arcade.SpriteList()
            self.turtle = arcade.SpriteList()
            for mushroom in self.mushroom:
                for turtle in self.turtle:
                    self.mushroom.remove(mushroom)
                    self.turtle.remove(turtle)

        if self.score_heart_number <= 0:
            self.game_over_flag = True
            self.coins = arcade.SpriteList()
            self.mushroom = arcade.SpriteList()
            self.turtle = arcade.SpriteList()
            for mushroom in self.mushroom:
                for turtle in self.turtle:
                    self.mushroom.remove(mushroom)
                    self.turtle.remove(turtle)

        # Обновление респавна грибов
        for respawn in self.mushroom_respawns[:]:
            respawn.count_mushroom_respawn -= delta_time
            if respawn.count_mushroom_respawn <= 0:
                mushroom = respawn.sprite
                new_mushroom = Mushroom()
                self.mushroom.append(new_mushroom)
                self.mushroom_respawns.remove(respawn)

        # Проверка коллизий с монетами
        for sprite in self.mario:
            for coin in self.coins[:]:
                if arcade.check_for_collision(sprite, coin):
                    self.coins.remove(coin)
                    self.score_number += 1
                    # Добавляем частицы
                    for _ in range(3):
                        self.particles.append(Particle(coin.center_x, coin.center_y))

            # Генерация монет
            if self.count_coin < 10:
                self.timer_coin += delta_time
                if self.timer_coin >= 3:
                    x = random.randint(50, self.width - 50)
                    y = self.height + 50
                    self.count_coin += 1
                    self.coins.append(Coin(x, y))
                    self.timer_coin = 0

        # Обновление позиций монет
        for coin in self.coins:
            coin.center_y -= coin.coin_speed * delta_time
            if coin.center_y < 115:
                coin.center_y = 115


def setup_game(width=1280, height=720, title="Mario"):
    game = MarioGame(width, height, title)
    return game


def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
