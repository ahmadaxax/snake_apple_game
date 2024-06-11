import pygame
from pygame.locals import *
import time
import random

class apple:
    def __init__(self,parent_screen):
        self.image = pygame.image.load('resources\\apple.jpg')
        self.parent_screen = parent_screen
        self.y=120
        self.x=120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*40
        self.y = random.randint(1,19)*40


class snake:
    def __init__(self, parent_screen, length):

        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources\\block.jpg').convert()
        self.direction = 'up'

        self.length = length
        self.x = [40]*length
        self.y = [40]*length


    def move_up(self):
       self.direction = 'up'
    def move_down(self):
       self.direction = 'down'
    def move_left(self):
       self.direction = 'left'
    def move_right(self):
        self.direction = 'right'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.y[i] = self.y[i-1]
            self.x[i] = self.x[i-1]

        if self.direction == 'up':
            self.y[0] -= 40
        if self.direction == 'down':
            self.y[0] += 40
        if self.direction == 'left':
            self.x[0] -= 40
        if self.direction == 'right':
            self.x[0] += 40
        self.draw()


    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = snake(self.surface,1)
        self.snake.draw()
        self.apple = apple(self.surface)
        self.apple.draw()
        self.pause = False
        self.level = 1
        self.speed = 0.3

    def play_background_music(self):
        pygame.mixer.music.load('resources\\bg_music_1.mp3')
        pygame.mixer.music.play()
    def play_sound(self,sound):
         sound = pygame.mixer.Sound("resources\\{}.mp3".format(sound))
         pygame.mixer.Sound.play(sound)
    def restart(self):
        self.snake = snake(self.surface, 1)
        self.apple = apple(self.surface)
        self.level = 1
        self.speed = 0.3

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + 40:
            if y1 >= y2 and y1 < y2 + 40:
                return True
        return False

    def render_background(self):
        bg=pygame.image.load('resources\\background.jpg')
        self.surface.blit(bg,(0,0))
    def play(self):
        self.render_background()

        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

            if self.snake.length % 3 == 0:
                self.level += 1
                self.speed = max(0.1, self.speed - 0.05)

        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "game over"
    def display_score(self):
        font = pygame.font.SysFont('Arial', 40)
        score = font.render(f'Score: {self.snake.length}', True, (255, 255, 255))
        level = font.render(f'Level: {self.level}', True, (255, 255, 255))
        self.surface.blit(score, (800, 10))
        self.surface.blit(level, (800, 60))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('Arial', 30)
        line1 = font.render("GAME OVER! Your score is %d " % self.snake.length, True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render('TO PLAY THE GAME PRESS ENTER . TO EXIT PRESS ESC', True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def show_pause_screen(self):
        font = pygame.font.SysFont('Arial', 30)
        line1 = font.render("GAME PAUSED", True, (255, 255, 255))
        self.surface.blit(line1, (400, 300))
        line2 = font.render('PRESS P TO RESUME', True, (255, 255, 255))
        self.surface.blit(line2, (400, 350))
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                   if event.key == K_ESCAPE:
                        running = False
                   elif event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                   elif event.key==K_p:
                       pause = not pause
                       if pause:
                           pygame.mixer.music.pause()
                           self.show_pause_screen()
                       else:
                           pygame.mixer.music.unpause()

                   elif not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                 self.play()
            except Exception as e:
                self.show_game_over()
                pause=True
                self.restart()


            time.sleep(self.speed)



if __name__=="__main__":
    game = Game()
    game.run()