import pygame
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Vizualizer')
clock = pygame.time.Clock()
crashed = False
zoombaSprite = pygame.image.load("Zoomba.png")
def car(x,y):
    gameDisplay.blit(zoombaSprite,(x,y))

while not crashed:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            crashed = True

        print(event)
    pygame.display.update()
    clock.tick(60)
