import pygame
from pygame.locals import *
import random

pygame.init()

# Set up the mixer (this is necessary to play sounds)
pygame.mixer.init()

# Load the music file
pygame.mixer.music.load('FlyGroove.mp3')

# Play the music
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load sound effects
fly_sound = pygame.mixer.Sound('fly.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Happy Humblebee')

# define font
font = pygame.font.SysFont('Comic Sans', 60)
small_font = pygame.font.SysFont('Comic Sans', 30)

# define colours
white = (255, 255, 255)

# define game variables
ground_scroll = 0
scroll_speed = 4
is_flying = False
is_game_over = False
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
high_score = 0
pipe_passed = False

# load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')


# function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    humblebee.rect.x = 100
    humblebee.rect.y = int(screen_height / 2)
    score = 0
    return score


class Humblebee(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"img/bee{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if is_flying:
            # apply gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not is_game_over:
            # jump
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
                fly_sound.play()  # Play fly sound
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handle the animation
            flap_cooldown = 5
            self.counter += 1

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            # rotate the bee
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            # point the bee at the ground
            self.image = pygame.transform.rotate(self.images[self.index], -90)

    def get_rect(self):
        # Return a smaller hitbox
        rect = self.rect.copy()
        rect.inflate_ip(-20, -20)  # reduce hitbox size
        return rect


class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        # position variable determines if the pipe is coming from the bottom or top
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


pipe_group = pygame.sprite.Group()
bee_group = pygame.sprite.Group()

humblebee = Humblebee(100, int(screen_height / 2))

bee_group.add(humblebee)

# create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:
    clock.tick(fps)

    # draw background
    screen.blit(bg, (0, 0))

    pipe_group.draw(screen)
    bee_group.draw(screen)
    bee_group.update()

    # draw and scroll the ground
    screen.blit(ground_img, (ground_scroll, 768))

    # check the score
    if len(pipe_group) > 0:
        if humblebee.get_rect().left > pipe_group.sprites()[0].rect.left and \
                humblebee.get_rect().right < pipe_group.sprites()[0].rect.right and \
                not pipe_passed:
            pipe_passed = True
        if pipe_passed:
            if humblebee.get_rect().left > pipe_group.sprites()[0].rect.right:
                score += 1
                pipe_passed = False
                if score > high_score:
                    high_score = score

    # draw the score in the middle of the screen
    draw_text(str(score), font, white, int(screen_width / 2 - font.size(str(score))[0] / 2), 20)
    # draw the highscore at the bottom left
    draw_text(f'Highscore: {high_score}', font, white, 10, screen_height - 80)

    # look for collision
    if pygame.sprite.groupcollide(bee_group, pipe_group, False, False) or humblebee.rect.top < 0:
        if not is_game_over:
            game_over_sound.play()  # Play game over sound
        is_game_over = True
    # once the bee has hit the ground it's game over and no longer flying
    if humblebee.rect.bottom >= 768:
        if not is_game_over:
            game_over_sound.play()  # Play game over sound
        is_game_over = True
        is_flying = False

    if is_game_over:
        draw_text('Game Over', font, white, int(screen_width / 2 - font.size('Game Over')[0] / 2), int(screen_height / 2 - font.size('Game Over')[1] / 2))
        if pygame.mouse.get_pressed()[0] == 1:  # Check if the action button is pressed
            is_game_over = False
            score = reset_game()

    if is_flying and not is_game_over:
        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        pipe_group.update()

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    # check for game over and reset
    if is_game_over:
        if pygame.mouse.get_pressed()[0] == 1:  # Check if the action button is pressed
            is_game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not is_flying and not is_game_over:
            is_flying = True

    pygame.display.update()

pygame.quit()
