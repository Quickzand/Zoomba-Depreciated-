import pygame, pathlib
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Vizualizer')
clock = pygame.time.Clock()
crashed = False
zoombaSprite = pygame.image.load(pathlib.Path().absolute + "/Zoomba.png")
def zoomba(x,y):
    gameDisplay.blit(zoombaSprite,(x,y))

while not crashed:
    zoomba(100,100)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            crashed = True

    pygame.display.update()
    clock.tick(60)
