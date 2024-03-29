import time
import pygame
from pygame.locals import *
import random

SIZE = 40
BACKGROUND_COLOR = (110,110,5)
class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resource/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(0,15)*SIZE
        self.y = random.randint(0,19)*SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resource/block.png").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))  # drawing the block on screen

    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if(self.direction == 'up'):
            self.y[0] -= SIZE
        if (self.direction == 'down'):
            self.y[0] += SIZE
        if (self.direction == 'left'):
            self.x[0] -= SIZE
        if (self.direction == 'right'):
            self.x[0] += SIZE
        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((640, 800))  # starts screen with size
        self.surface.fill(BACKGROUND_COLOR)  # screen color
        self.snake = Snake(self.surface, 5)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2  and  x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resource/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resource/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resource/background.jpg")
        self.surface.blit(bg,(0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        #snake colliding with apple
        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()
        #snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score,(520,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is  {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (150, 320))
        line2 = font.render(f"To play again press Enter. To exit pres Escape", True, (255,255,255))
        self.surface.blit(line2, (70, 370))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 5)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.play_background_music()

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
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
                pause = True
                self.reset()
            time.sleep(.15)

if __name__ == "__main__":
    game = Game()
    game.run()

