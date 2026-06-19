from constants import *

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
