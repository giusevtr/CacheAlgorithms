import pygame
import sys
from algorithms.MARKING import MARKING
from algorithms.LRU import LRU
from algorithms.ARC import ARC
from algorithms.WALK_MARKING import WALK_MARKING
from algorithms.PAGERANK_MARKING import PAGERANK_MARKING
from algorithms.PAGERANK_MARKING2 import PAGERANK_MARKING2

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Algorithm animation')
clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

textSize = 26
tileSize = (100,50)
separation = 30

## Get paraments
## Must specify algorithm use and cache size
if len(sys.argv) < 2 :
    print("Error: Must supply algorithm name and cache size.")
    print("usage: python3 algo_animation.py [algorithm] [cache_size]")
    exit(1)

algorithm = sys.argv[1]
cache_size = int(sys.argv[2])

if algorithm.lower() == 'arc' :
    algo = ARC(cache_size)
elif algorithm.lower() == 'marking' :
    algo = MARKING(cache_size)
elif algorithm.lower() == 'lru' :
    algo = LRU(cache_size)
elif algorithm.lower() == 'walk' :
    algo = WALK_MARKING(cache_size)
elif algorithm.lower() == 'pagerank2' :
    algo = PAGERANK_MARKING2(cache_size)


def draw_tile(page, pos, color_id=0) :
    txtsz = textSize * len(page)
    myfont = pygame.font.SysFont("monospace", textSize)
    # render text
    # label = myfont.render(page[0], 2, white)
    label = myfont.render(page, 2, white)

    # textpos = (pos[0] + tileSize[0]/2 - txtsz/2,pos[1] + tileSize[1]/2 - txtsz/2)
    textpos = (pos[0] + 3, pos[1] + tileSize[1]/2 - textSize/2)

    gameDisplay.blit(label, textpos)

    if color_id == 0 :
        color = white
    elif color_id == 1:
        color = red
    elif color_id == 2:
        color = black
    elif color_id == 3:
        color = blue

    pygame.draw.rect(gameDisplay, color,pos + tileSize,4)

crashed = False
tilepos_x = 10

while not crashed :

    q = None

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            key = str(event.type)
            if (event.key >= ord('a') and event.key <= ord('z')) or (event.key >= ord('A') and event.key <= ord('Z')):
                q = chr(event.key)

    if q != None :
        algo.request(q)

    gameDisplay.fill(black)

    X = 0
    Y = 0
    for L in algo.get_data() :
        for p in L :
            # pygame.draw.rect(gameDisplay, white,(tilepos_x,20) + tileSize,1)

            # draw_tile(p, (X,Y) , algo.page_color(p))
            draw_tile(algo.page_label(p), (X,Y) , algo.page_color(p))

            X = X + tileSize[0]
        Y = Y + tileSize[1] + separation
        X = 0
    pygame.display.update()
    clock.tick(30)


pygame.quit()
quit()
