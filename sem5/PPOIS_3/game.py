from constants import *
from ghost import  *
from buttons import  Button


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if ghosts_frozen:  # Frozen state - white ghosts
            if flicker and ghosts_frozen_counter < 100:
                screen.blit(frozen_ghost_images[0], (self.x_pos, self.y_pos))
            else:
                screen.blit(frozen_ghost_images[2], (self.x_pos, self.y_pos))
        elif (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            if self.direction == LEFT:
                screen.blit(self.img[0], (self.x_pos, self.y_pos))
            if self.direction == RIGHT:
                screen.blit(self.img[2], (self.x_pos, self.y_pos))
            if self.direction == DOWN:
                screen.blit(self.img[3], (self.x_pos, self.y_pos))
            if self.direction == UP:
                screen.blit(self.img[1], (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            if power_counter > 420 and flicker:
                screen.blit(frozen_ghost_images[2], (self.x_pos, self.y_pos))
            else:
                screen.blit(frozen_ghost_images[1], (self.x_pos, self.y_pos)) 
        else:
            if self.direction == LEFT:
                screen.blit(eaten_ghost_images[0], (self.x_pos, self.y_pos))
            if self.direction == RIGHT:
                screen.blit(eaten_ghost_images[2], (self.x_pos, self.y_pos))
            if self.direction == DOWN:
                screen.blit(eaten_ghost_images[3], (self.x_pos, self.y_pos))
            if self.direction == UP:
                screen.blit(eaten_ghost_images[1], (self.x_pos, self.y_pos))

        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (20, 20))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if LEFT < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == DOOR:
                self.turns[DOWN] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < UP \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == DOOR and (
                    self.in_box or self.dead)):
                self.turns[RIGHT] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < UP \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == DOOR and (
                    self.in_box or self.dead)):
                self.turns[LEFT] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < UP \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == DOOR and (
                    self.in_box or self.dead)):
                self.turns[UP] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < UP \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == DOOR and (
                    self.in_box or self.dead)):
                self.turns[DOWN] = True

            if self.direction == DOWN or self.direction == UP:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < UP \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == DOOR and (
                            self.in_box or self.dead)):
                        self.turns[UP] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < UP \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == DOOR and (
                            self.in_box or self.dead)):
                        self.turns[DOWN] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < UP \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == DOOR and (
                            self.in_box or self.dead)):
                        self.turns[RIGHT] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < UP \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == DOOR and (
                            self.in_box or self.dead)):
                        self.turns[LEFT] = True

            if self.direction == LEFT or self.direction == RIGHT:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < UP \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == DOOR and (
                            self.in_box or self.dead)):
                        self.turns[UP] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < UP \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == DOOR and (
                            self.in_box or self.dead)):
                        self.turns[DOWN] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < UP \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == DOOR and (
                            self.in_box or self.dead)):
                        self.turns[RIGHT] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < UP \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == DOOR and (
                            self.in_box or self.dead)):
                        self.turns[LEFT] = True
        else:
            self.turns[LEFT] = True
            self.turns[RIGHT] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box


    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
        if self.direction == LEFT:
            if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                self.x_pos += self.speed
            elif not self.turns[LEFT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
            elif self.turns[LEFT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                if self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == RIGHT:
            if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                self.direction = UP
            elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                self.x_pos -= self.speed
            elif not self.turns[RIGHT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[RIGHT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                if self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == DOWN:
            if self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                self.direction = RIGHT
                self.x_pos -= self.speed
            elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                self.direction = DOWN
                self.y_pos -= self.speed
            elif not self.turns[DOWN]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[DOWN]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[1]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == UP:
            if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                self.y_pos += self.speed
            elif not self.turns[UP]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[UP]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == LEFT:
            if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                self.x_pos += self.speed
            elif not self.turns[LEFT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
            elif self.turns[LEFT]:
                self.x_pos += self.speed
        elif self.direction == RIGHT:
            if self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                self.x_pos -= self.speed
            elif not self.turns[RIGHT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[RIGHT]:
                self.x_pos -= self.speed
        elif self.direction == DOWN:
            if self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                self.direction = DOWN
                self.y_pos -= self.speed
            elif not self.turns[DOWN]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
            elif self.turns[DOWN]:
                self.y_pos -= self.speed
        elif self.direction == UP:
            if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                self.y_pos += self.speed
            elif not self.turns[UP]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
            elif self.turns[UP]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
        if self.direction == LEFT:
            if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                self.x_pos += self.speed
            elif not self.turns[LEFT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
            elif self.turns[LEFT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                if self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == RIGHT:
            if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                self.direction = UP
            elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                self.x_pos -= self.speed
            elif not self.turns[RIGHT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[RIGHT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                if self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == DOWN:
            if self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                self.direction = DOWN
                self.y_pos -= self.speed
            elif not self.turns[DOWN]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[DOWN]:
                self.y_pos -= self.speed
        elif self.direction == UP:
            if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                self.y_pos += self.speed
            elif not self.turns[UP]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[UP]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == LEFT:
            if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                self.x_pos += self.speed
            elif not self.turns[LEFT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
            elif self.turns[LEFT]:
                self.x_pos += self.speed
        elif self.direction == RIGHT:
            if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                self.direction = UP
            elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                self.x_pos -= self.speed
            elif not self.turns[RIGHT]:
                if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[RIGHT]:
                self.x_pos -= self.speed
        elif self.direction == DOWN:
            if self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                self.direction = RIGHT
                self.x_pos -= self.speed
            elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                self.direction = DOWN
                self.y_pos -= self.speed
            elif not self.turns[DOWN]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.target[RIGHT] > self.y_pos and self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[UP]:
                    self.direction = UP
                    self.y_pos += self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[DOWN]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == UP:
            if self.target[RIGHT] > self.y_pos and self.turns[UP]:
                self.y_pos += self.speed
            elif not self.turns[UP]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.target[RIGHT] < self.y_pos and self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[DOWN]:
                    self.direction = DOWN
                    self.y_pos -= self.speed
                elif self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                elif self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
            elif self.turns[UP]:
                if self.target[LEFT] > self.x_pos and self.turns[LEFT]:
                    self.direction = LEFT
                    self.x_pos += self.speed
                elif self.target[LEFT] < self.x_pos and self.turns[RIGHT]:
                    self.direction = RIGHT
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos =-30
        return self.x_pos, self.y_pos, self.direction


def show_leaderboard():
    leaderboard_active = True
    leader_font = pygame.font.Font('freesansbold.ttf', 24)
    back_button = Button(WIDTH//2 - displacement_100, HEIGHT - displacement_100, 200, 50, "Назад" , click_sound, "back")
    
    while leaderboard_active:
        screen.fill(BG_COLOR)
        
        title = font.render("Таблица лидеров", True, TEXT_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        
        # Вывод лидеров
        for i, leader in enumerate(leaderboard):
            text = leader_font.render(f"{i+1}. {leader['name']} - {leader['score']}", True, TEXT_COLOR)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 150 + i*50))
        
        # Кнопка назад
        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            action = back_button.handle_event(event)
            if action == "back":
                leaderboard_active = False
        
        pygame.display.flip()
        timer.tick(fps)
    
    return True

def get_player_name(score):
    name = ""
    input_active = True
    input_font = pygame.font.Font('freesansbold.ttf', 32)
    
    while input_active:
        screen.fill(BG_COLOR)
        
        prompt_text = font.render("Введите ваше имя:", True, TEXT_COLOR)
        score_text = font.render(f"Ваш счет: {score}", True, TEXT_COLOR)
        name_text = input_font.render(name, True, TEXT_COLOR)
        
        screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, HEIGHT//2 - displacement_100))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(name_text, (WIDTH//2 - name_text.get_width()//2, HEIGHT//2))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ""
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15:  # Ограничение длины имени
                        name += event.unicode
        
        pygame.display.flip()
        timer.tick(fps)
    
    return name

def update_leaderboard(name, score):
    global leaderboard
    
    leaderboard.append({"name": name, "score": score})
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    
    while len(leaderboard) > 5:
        leaderboard.pop()
    
    # Сохраняем обновленную таблицу лидеров
    from constants import save_leaderboard
    save_leaderboard(leaderboard)

def show_game_result(result_text, score=0):
    result_active = True
    result_font = pygame.font.Font('freesansbold.ttf', 36)
    menu_button = Button(WIDTH//2 - 150, HEIGHT//2 + displacement_100, 300, 50, "В главное меню", click_sound, "menu")
    
    if "победил" in result_text.lower():
        player_name = get_player_name(score)
        if player_name:
            update_leaderboard(player_name, score)
    
    while result_active:
        screen.fill(BG_COLOR)
        
        text = result_font.render(result_text, True, HOVER_COLOR)
        score_text = font.render(f"Счет: {score}", True, TEXT_COLOR)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
        
        mouse_pos = pygame.mouse.get_pos()
        menu_button.check_hover(mouse_pos)
        menu_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            action = menu_button.handle_event(event)
            if action == "menu":
                result_active = False
        
        pygame.display.flip()
        timer.tick(fps)
    
    return True

def show_pause_menu():
    pause_active = True
    continue_button = Button(WIDTH//2 - 150, HEIGHT//2 - 60, 300, 50, "Продолжить", click_sound, "continue")
    menu_button = Button(WIDTH//2 - 150, HEIGHT//2 + 20, 300, 50, "Главное меню", click_sound, "menu")
    
    while pause_active:
        screen.fill(BG_COLOR)
        
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        screen.blit(s, (0, 0))
        
        title = font.render("Игра на паузе", True, HOVER_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 120))
        
        mouse_pos = pygame.mouse.get_pos()
        continue_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)
        
        continue_button.draw(screen)
        menu_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            
            action = continue_button.handle_event(event)
            if action == "continue":
                return "continue"
            
            action = menu_button.handle_event(event)
            if action == "menu":
                return "menu"
        
        pygame.display.flip()
        timer.tick(fps)
    
    return "continue"

def reset_game():
    global player_x, player_y, direction, direction_command, blinky_x, blinky_y, blinky_direction
    global inky_x, inky_y, inky_direction, pinky_x, pinky_y, pinky_direction, clyde_x, clyde_y, clyde_direction
    global eaten_ghost, blinky_dead, inky_dead, clyde_dead, pinky_dead, score, lives, level
    global powerup, power_counter, startup_counter, moving, game_over, game_won, death_animation, death_counter
    global sound_played, music_started, controls_reversed, controls_reversed_counter, ghosts_frozen, ghosts_frozen_counter
    global leaderboard
    
    # Загружаем актуальную таблицу лидеров
    from constants import load_leaderboard
    leaderboard = load_leaderboard()
    
    death_animation = False
    death_counter = 0
    sound_played = False
    music_started = False
    pygame.mixer.music.stop() 
    player_x = 438
    player_y = 495
    direction = 0
    direction_command = 0
    blinky_x = 56
    blinky_y = 58
    blinky_direction = 0
    inky_x = 440
    inky_y = 388
    inky_direction = 2
    pinky_x = 380
    pinky_y = 438
    pinky_direction = 2
    clyde_x = 440
    clyde_y = 438
    clyde_direction = 2
    eaten_ghost = [False, False, False, False]
    blinky_dead = False
    inky_dead = False
    clyde_dead = False
    pinky_dead = False
    score = 0
    lives = 3
    level = copy.deepcopy(current_board)
    powerup = False
    power_counter = 0
    startup_counter = 0
    moving = False
    game_over = False
    game_won = False
    controls_reversed = False
    controls_reversed_counter = 0
    ghosts_frozen = False
    ghosts_frozen_counter = 0

def show_rules():
    rules_active = True
    rules_font = pygame.font.Font('freesansbold.ttf', 20)
    back_button = Button(WIDTH//2 - displacement_100, HEIGHT - displacement_100, 200, 50, "Назад", click_sound, "back")
    
    rules_text = [
        "Правила игры Pac-Man:",
        "",
        "1. Управляйте Пакманом с помощью клавиш WASD",
        "2. Собирайте точки для получения очков",
        "3. Большие точки дают временную неуязвимость,",
        "заморозку без неуязвимости или инверсию управления",
        "4. Избегайте привидений в обычном режиме",
        "5. В режиме неуязвимости можно съесть привидений",
        "6. За каждое съеденное привидение получаете бонусные очки",
        "",
        "Цель игры: набрать как можно больше очков!"
    ]
    
    while rules_active:
        screen.fill(BG_COLOR)
        
        for i, line in enumerate(rules_text):
            text = rules_font.render(line, True, TEXT_COLOR)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 50 + i*30))
        
        mouse_pos = pygame.mouse.get_pos()
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            action = back_button.handle_event(event)
            if action == "back":
                rules_active = False
        
        pygame.display.flip()
        timer.tick(fps)
    
    return True

def main_menu():
    global current_board, color, MAP_BUTTON_COLOR
    
    menu_active = True
    death_animation_menu = False
    death_counter_menu = 0
    
    # Создаем кнопку для переключения карт
    board_button = Button(700, 900, displacement_100, 40, "Карта", click_sound, "switch_map")
    
    buttons = [
        Button(WIDTH//2 - 150, 200, 300, 50, "Начать игру", click_sound, "start"),
        Button(WIDTH//2 - 150, 280, 300, 50, "Таблица лидеров", click_sound, "leaderboard"),
        Button(WIDTH//2 - 150, 360, 300, 50, "Правила", click_sound, "rules"),
        Button(WIDTH//2 - 150, 440, 300, 50, "Выйти", click_sound, "quit"),
        Button(360, 590, 200, 200, "", uhh_sound, "pacman_dead"),
        board_button  # Добавляем кнопку переключения карты
    ]
    
    title_font = pygame.font.Font('freesansbold.ttf', 48)
    title = title_font.render("PAC-MAN", True, HOVER_COLOR)
    counter1 = 0
    
    while menu_active:
        screen.fill(BG_COLOR)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))

        if not death_animation_menu:
            if counter1 < 19:
                counter1 += 1     
            else:
                counter1 = 0
            screen.blit(pygame.transform.scale(player_images[counter1 // 5], (200, 200)), (360,590))
        else:
            if death_counter_menu < 60:
                frame_index = death_counter_menu // 5
                if frame_index < len(dead_packman_images):
                    screen.blit(pygame.transform.scale(dead_packman_images[frame_index], (200, 200)), (360,590))
                death_counter_menu += 1
            else:
                death_animation_menu = False
                death_counter_menu = 0

        mouse_pos = pygame.mouse.get_pos()
        
        for button in buttons:
            button.check_hover(mouse_pos)
            if button.text != "":
                if button == board_button:
                    # Специальное отображение для кнопки карты
                    btn_color = CORAL_COLOR if current_board == board_2 else MENU_COLOR
                    pygame.draw.rect(screen, btn_color, button.rect, border_radius=10)
                    pygame.draw.rect(screen, TEXT_COLOR, button.rect, 2, border_radius=10)
                    text_surf = font.render(button.text, True, TEXT_COLOR)
                    text_rect = text_surf.get_rect(center=button.rect.center)
                    screen.blit(text_surf, text_rect)
                else:
                    button.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            for button in buttons:
                action = button.handle_event(event)
                if action == "start":
                    return True
                elif action == "leaderboard":
                    if not show_leaderboard():
                        return False
                elif action == "rules":
                    if not show_rules():
                        return False
                elif action == "quit":
                    pygame.quit()
                    return False
                elif action == "pacman_dead" and not death_animation_menu:
                    death_animation_menu = True
                    death_counter_menu = 0
                elif action == "switch_map":
                    # Переключаем карту и обновляем цвет
                    if current_board == boards:
                        current_board = board_2
                        color = CORAL_COLOR  # Коралловый цвет для второй карты
                    else:
                        current_board = boards
                        color = 'blue'  # Синий цвет для первой карты
                    click_sound.play()
        
        pygame.display.flip()
        timer.tick(fps)
    
    return True


def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))


def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
            get_random_powerup_sound().play()
        if level[center_y // num1][center_x // num2] == -1:  
            level[center_y // num1][center_x // num2] = 0
            scor += 200
            global controls_reversed, controls_reversed_counter
            controls_reversed = True
            controls_reversed_counter = 720  
            reverse_movement.play()
        if level[center_y // num1][center_x // num2] == -2:  
            level[center_y // num1][center_x // num2] = 0
            scor += 200
            global ghosts_frozen, ghosts_frozen_counter
            ghosts_frozen = True
            ghosts_frozen_counter = 360  
            get_random_powerup_sound().play()
            
        game_won = True
        for row in level:
            if 1 in row or 2 in row or -1 in row or -2 in row:
                game_won = False
                break
        if game_won:
            victory_sound.play()
            
    return scor, power, power_count, eaten_ghost

# Обновляем функцию draw_board()
def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == -1:  # Purple dot - reverse controls
                size = 8 + (2 * math.sin(pygame.time.get_ticks() * 0.005))  # Pulsation effect
                pygame.draw.circle(screen, (128, 0, 128), (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), int(size))
            if level[i][j] == -2:  # Light blue dot - freeze ghosts
                size = 8 + (2 * math.sin(pygame.time.get_ticks() * 0.005))  # Pulsation effect
                pygame.draw.circle(screen, (173, 216, 230), (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), int(size))
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == DOOR:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 3)


def draw_player():
    # LEFT-RIGHT, RIGHT-LEFT, DOWN-UP, UP-DOWN
    if direction == LEFT:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == RIGHT:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == DOWN:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == UP:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == LEFT:
            if level[centery // num1][(centerx - num3) // num2] < UP:
                turns[RIGHT] = True
        if direction == RIGHT:
            if level[centery // num1][(centerx + num3) // num2] < UP:
                turns[LEFT] = True
        if direction == DOWN:
            if level[(centery + num3) // num1][centerx // num2] < UP:
                turns[UP] = True
        if direction == UP:
            if level[(centery - num3) // num1][centerx // num2] < UP:
                turns[DOWN] = True

        if direction == DOWN or direction == UP:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < UP:
                    turns[UP] = True
                if level[(centery - num3) // num1][centerx // num2] < UP:
                    turns[DOWN] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < UP:
                    turns[RIGHT] = True
                if level[centery // num1][(centerx + num2) // num2] < UP:
                    turns[LEFT] = True
        if direction == LEFT or direction == RIGHT:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < UP:
                    turns[UP] = True
                if level[(centery - num1) // num1][centerx // num2] < UP:
                    turns[DOWN] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < UP:
                    turns[RIGHT] = True
                if level[centery // num1][(centerx + num3) // num2] < UP:
                    turns[LEFT] = True
    else:
        turns[LEFT] = True
        turns[RIGHT] = True

    return turns


def move_player(play_x, play_y):
    # r, l, u, d
    if direction == LEFT and turns_allowed[LEFT]:
        play_x += player_speed
    elif direction == RIGHT and turns_allowed[RIGHT]:
        play_x -= player_speed
    if direction == DOWN and turns_allowed[DOWN]:
        play_y -= player_speed
    elif direction == UP and turns_allowed[UP]:
        play_y += player_speed
    return play_x, play_y


def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

game_active = True
while game_active:

    if not main_menu():
        game_active = False
        break

    reset_game()  # Сбрасываем игру перед началом

    run = True
    while run:
        timer.tick(fps)
        
        # Воспроизводим фоновую музыку, если игра началась
        if not music_started and startup_counter >= 240:
            pygame.mixer.music.play(-1)
            music_started = True
        
        if counter < 19:
            counter += 1
            if counter > 10:
                flicker = False
        else:
            counter = 0
            flicker = True
            
        if powerup and power_counter < 600:
            power_counter += 1
        elif powerup and power_counter >= 600:
            power_counter = 0
            powerup = False
            eaten_ghost = [False, False, False, False]
            

        if game_over or game_won:
            pygame.mixer.music.stop()
            
            if game_over and not death_animation:
                death_animation = True
                death_counter = 0
                death_sound.play()
            elif game_won:
                victory_sound.play()
            
            if death_animation:
                if death_counter < 120:
                    screen.fill('black')
                    draw_board()
                    draw_misc()
                    
                    frame_index = death_counter // 10
                    if frame_index < len(dead_packman_images):
                        screen.blit(dead_packman_images[frame_index], (player_x, player_y))
                    
                    death_counter += 1
                    pygame.display.flip()
                    continue
                else:
                    if not show_game_result("Вы проиграли!", score):
                        run = False
                    break
            else:
                result_text = "Вы победили!"
                if not show_game_result(result_text, score):
                    run = False
                break

        screen.fill('black')
        draw_board()

        if startup_counter < 240 and not game_over and not game_won:
            moving = False
            if not sound_played:
                start_sound.play()
                sound_played = True
            
            if startup_counter % 20 < 10:
                ready_text = font.render("Ready?", True, 'yellow')
                screen.blit(pygame.transform.scale(ready_text, (120, 40)), (400,330))
            
            startup_counter += 1
        else:
            moving = True


        center_x = player_x + 23
        center_y = player_y + 24
        if powerup:
            ghost_speeds = [1, 1, 1, 1]
        else:
            ghost_speeds = [2, 2, 2, 2]
        if eaten_ghost[0]:
            ghost_speeds[0] = 2
        if eaten_ghost[1]:
            ghost_speeds[1] = 2
        if eaten_ghost[2]:
            ghost_speeds[2] = 2
        if eaten_ghost[3]:
            ghost_speeds[3] = 2
        if blinky_dead:
            ghost_speeds[0] = 4
        if inky_dead:
            ghost_speeds[1] = 4
        if pinky_dead:
            ghost_speeds[2] = 4
        if clyde_dead:
            ghost_speeds[3] = 4

        game_won = True
        for i in range(len(level)):
            if 1 in level[i] or 2 in level[i]:
                game_won = False


        player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
        draw_player()
        blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_images, blinky_direction, blinky_dead,
                    blinky_box, 0)
        inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_images, inky_direction, inky_dead,
                    inky_box, 1)
        pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_images, pinky_direction, pinky_dead,
                    pinky_box, 2)
        clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_images, clyde_direction, clyde_dead,
                    clyde_box, 3)
        draw_misc()
        targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)

        turns_allowed = check_position(center_x, center_y)
        if moving:
            player_x, player_y = move_player(player_x, player_y)
            if not ghosts_frozen:  
                if not blinky_dead and not blinky.in_box:
                    blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
                else:
                    blinky_x, blinky_y, blinky_direction = blinky.move_clyde()
                if not pinky_dead and not pinky.in_box:
                    pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
                else:
                    pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
                if not inky_dead and not inky.in_box:
                    inky_x, inky_y, inky_direction = inky.move_inky()
                else:
                    inky_x, inky_y, inky_direction = inky.move_clyde()
                clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
            else:  
                blinky.draw()
                pinky.draw()
                inky.draw()
                clyde.draw()

        
        score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

        
        if not powerup:
            if (player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                    (player_circle.colliderect(inky.rect) and not inky.dead) or \
                    (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                    (player_circle.colliderect(clyde.rect) and not clyde.dead):
                if lives > 1:  
                    lives -= 1
                    startup_counter = 0
                    powerup = False
                    power_counter = 0
                    player_x = 450
                    player_y = 663
                    direction = 0
                    direction_command = 0
                    blinky_x = 56
                    blinky_y = 58
                    blinky_direction = 0
                    inky_x = 440
                    inky_y = 388
                    inky_direction = 2
                    pinky_x = 440
                    pinky_y = 438
                    pinky_direction = 2
                    clyde_x = 440
                    clyde_y = 438
                    clyde_direction = 2
                    eaten_ghost = [False, False, False, False]
                    blinky_dead = False
                    inky_dead = False
                    clyde_dead = False
                    pinky_dead = False
                    controls_reversed = False
                    uhh_sound.play()  # Звук при потере жизни (но не последней)
                else:  # Если это последняя жизнь
                    game_over = True
                    moving = False
                    startup_counter = 0
                    controls_reversed = False
                    

        if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
            blinky_dead = True
            eaten_ghost[0] = True
            score += (2 ** eaten_ghost.count(True)) * score_modifier
            ghost_eat_sound.play()  # Звук поедания привидения
        if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
            inky_dead = True
            eaten_ghost[1] = True
            score += (2 ** eaten_ghost.count(True)) * score_modifier
            ghost_eat_sound.play()
        if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
            pinky_dead = True
            eaten_ghost[2] = True
            score += (2 ** eaten_ghost.count(True)) * score_modifier
            ghost_eat_sound.play()
        if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
            clyde_dead = True
            eaten_ghost[3] = True
            score += (2 ** eaten_ghost.count(True)) * score_modifier
            ghost_eat_sound.play()


        if controls_reversed:
            controls_reversed_counter -= 1
            if controls_reversed_counter <= 0:
                controls_reversed = False
                
        if ghosts_frozen:
            ghosts_frozen_counter -= 1
            if ghosts_frozen_counter <= 0:
                ghosts_frozen = False
        
        # Обработка ввода с учетом reversed controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game_active = False
            if event.type == pygame.KEYDOWN:
                if not controls_reversed:  # Нормальное управление
                    if event.key == pygame.K_d:
                        direction_command = 0
                    if event.key == pygame.K_a:
                        direction_command = 1
                    if event.key == pygame.K_w:
                        direction_command = 2
                    if event.key == pygame.K_s:
                        direction_command = 3
                else:  # Обратное управление
                    if event.key == pygame.K_d:
                        direction_command = 1  
                    if event.key == pygame.K_a:
                        direction_command = 0  
                    if event.key == pygame.K_w:
                        direction_command = 3  
                    if event.key == pygame.K_s:
                        direction_command = 2  
   
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    result = show_pause_menu()
                    if result == "menu":
                        run = False
                    elif result == "quit":
                        run = False
                        game_active = False
                    else:
                        pygame.mixer.music.unpause()

        if direction_command == 0 and turns_allowed[0]:
            direction = 0
        if direction_command == 1 and turns_allowed[1]:
            direction = 1
        if direction_command == 2 and turns_allowed[2]:
            direction = 2
        if direction_command == 3 and turns_allowed[3]:
            direction = 3

        if player_x > 900:
            player_x = -30
        elif player_x < -30:
            player_x = 900

        if blinky.in_box and blinky_dead:
            blinky_dead = False
        if inky.in_box and inky_dead:
            inky_dead = False
        if pinky.in_box and pinky_dead:
            pinky_dead = False
        if clyde.in_box and clyde_dead:
            clyde_dead = False

        pygame.display.flip()
pygame.quit()

