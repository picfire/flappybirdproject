import pygame
from sys import exit
import random
# game variables
width, height = 360, 640

#bird class
birdx = width/8
birdy = height/2
birdwidth = 34
birdheight = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self,birdx,birdy,birdwidth,birdheight)
        self.img = img
#pipe class
pipex = width
pipey = 0
pipewidth = 64
pipeheight = 512

class Pipe(pygame.Rect):
    def __init__(self,img):
        pygame.Rect.__init__(self,pipex,pipey,pipewidth,pipeheight)
        self.img = img
        self.passed = False

#images
flappy = pygame.image.load("flappybird.png")
flappy = pygame.transform.scale(flappy, (birdwidth,birdheight))
background_img = pygame.image.load("background.jpg")
blacbg = pygame.image.load("blackbg2.jpg")
top_pipe_img = pygame.image.load("toppipe.png")
top_pipe_img = pygame.transform.scale(top_pipe_img,(pipewidth,pipeheight))
bot_pipe_img = pygame.image.load("bottompipe.png")
bot_pipe_img = pygame.transform.scale(bot_pipe_img,(pipewidth,pipeheight))


background_img.set_alpha(30)

#logical structure
bird = Bird(flappy)
pipes = []
velocity_x = -2
velocity_y = 0
gravity = 0.4
score = 0
game_over = False

def draw():
    window.blit(blacbg,(0,-420))
    window.blit(background_img, (0,0))
    window.blit(bird.img, bird)

    for pipe in pipes:
        window.blit(pipe.img, pipe)
    text_str = str(int(score))

    if game_over:
        text_str = "Game Over: " + text_str

    text_font = pygame.font.SysFont("Comic Sans MS", 45)
    text_render = text_font.render(text_str,True, "white")
    window.blit(text_render,(5,0))

def move():
    global velocity_y, score, game_over
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y > height:
        game_over = True
        return
    for pipe in pipes:
        pipe.x += velocity_x
        if not pipe.passed and bird.x > pipe.x+ pipe.width:
            score += 0.5 # 0.5 because there are two pipes top and bottom so total is 1
            pipe.passed = True
        if bird.colliderect(pipe):
            game_over = True
            return
    while len(pipes) > 0 and pipes[0].x + pipewidth < 0:
        pipes.pop(0)
        


def CreatePipes():

    rand_pipe_y = pipey - pipeheight/4 - random.random()*(pipeheight/2) # 0- height/2
    opening_space = height/4



    top_pipe = Pipe(top_pipe_img)
    top_pipe.y = rand_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bot_pipe_img)
    bottom_pipe.y = top_pipe.y + top_pipe.height + opening_space
    pipes.append(bottom_pipe)

    print(len(pipes))



pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("CIEE Flappy Bird")
clock = pygame.time.Clock()

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500) 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == create_pipes_timer and not game_over:
            CreatePipes()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                velocity_y -= 6

                #reset

                if game_over:
                    bird.y = birdy
                    pipes.clear()
                    game_over= False
                    score = 0


    if not game_over: 
        move()
        draw()
        pygame.display.update()
        clock.tick(60)


