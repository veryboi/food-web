import math
import pygame
from math import pi
import PyParticles
import poly_point_isect
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 7000

pygame.init()

universe = PyParticles.Environment((SCREEN_WIDTH, SCREEN_HEIGHT))
universe.colour = (255, 255, 255)
universe.addFunctions(['move', 'bounce', 'collide', 'drag', 'accelerate', 'attract'])
universe.acceleration = (pi, 0)
universe.mass_of_air = 10
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen_rect = screen.get_rect()

pygame.display.set_caption("web boi")


def text_to_screen(screen, text, x, y, size = 20,
    color = (0,0,0), font_type = 'arial'):

    text = str(text)
    font = pygame.font.SysFont(font_type, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()

    screen.blit(text, (x-text_rect.width//2, y - text_rect.height//2))

def draw_arrow(screen, start2, end2, colour=(0,0,0)):
    start = start2.copy()
    end = end2.copy()
    x_diff = -start[0] + end[0]
    y_diff = -start[1] + end[1]
    distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
    cutoff = 20
    if distance > cutoff:
        #print(distance)
        # proportion = 0.8
        # end[0] = int(start[0] + proportion * x_diff)
        # end[1] = int(start[1] + proportion * y_diff)

        end[0] = int(end[0] - cutoff * x_diff/distance)
        end[1] = int(end[1] - cutoff * y_diff/distance)
        #print(start[0]- end[0], start[1] - end[1])
        #print(end[0], end[1])

    pygame.draw.aaline(screen,colour,start,end,2)
    rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    scale = 5
    pygame.draw.polygon(screen, (0, 0, 0), ((end[0]+scale*math.sin(math.radians(rotation)), end[1]+scale*math.cos(math.radians(rotation))), (end[0]+scale*math.sin(math.radians(rotation-120)), end[1]+scale*math.cos(math.radians(rotation-120))), (end[0]+scale*math.sin(math.radians(rotation+120)), end[1]+scale*math.cos(math.radians(rotation+120)))))


class animal:
    def __init__(self, name):
        self.name = name

    def addDiet(self, diets):
        self.diets = diets



allStuff = [
    "bat",
    "muskrat",
    "cattail",
    "bulrush",
    "duck",
    "hawk",
    "clam",
    "beetle",
    "turtle",
    "fish",
    "snake",
    "peeper",
    "mosquito",
    "algae",
    "sora",
    "milkweed",
    "bird"
]

diets = [
    ("mosquito", "beetle"),
    ("cattail", "bulrush", "peeper", "clam"),
    (),
    (),
    ("clam", "cattail", "peeper", "fish"),
    ("peeper", "bird", "snake", "muskrat"),
    ("algae", "mosquito"),
    ("milkweed",),
    ("mosquito", "beetle", "clam", "peeper"),
    ("mosquito",),
    ("peeper", "fish"),
    ("beetle",),
    ("milkweed","muskrat", "bat"),
    (),
    ("mosquito", "bulrush", "clam"),
    (),
    ("mosquito", "cattail")
]

indexDict = {

}
for i in range(len(allStuff)):
    indexDict[allStuff[i]] = i
clock = pygame.time.Clock()
counter = 0
for i in range(4):
    for y in range(5):
        #print(5 * i + y)
        if counter < 17:
            counter += 1
            left = i * 240
            top = y * 240
            print(5 * i + y - 1)
            universe.addParticles(mass=1000, size=1, speed=10, elasticity=0.1, colour=(20, 40, 200),  val=allStuff[5 * i + y ])


        else:
            break
totalReceivers = {}

for i in range(len(allStuff)):
    totalReceivers[allStuff[i]] = diets[i]

print(totalReceivers)

for pred, preys in totalReceivers.items():
    for prey in preys:
        universe.addSpring( indexDict[pred],indexDict[prey], length=100, strength=0.5)
cool_gradient = 0


running = True
current_dragged = False
selected_particle = None
paused = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                universe.mass_of_air=10000
                print('down')
            else:
                universe.mass_of_air = 10
        if event.type == pygame.MOUSEBUTTONDOWN:
            selected_particle = universe.findParticle(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None

    if selected_particle:
        selected_particle.mouseMove(pygame.mouse.get_pos())
    if not paused:
        universe.update()

    screen.fill(universe.colour)

    for p in universe.particles:
        #pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, 0)
        text_to_screen(screen, p.val, int(p.x), int(p.y))
    tot_speed = 0
    for particle in universe.particles:
        tot_speed += particle.speed
    if tot_speed > 3:
        text_to_screen(screen, "Speed till equilibrium: " + str(round(tot_speed-3, 3)), 500,20)
    else:
        text_to_screen(screen, "Equilibrium!", 500, 20)

    segments = []
    for s in universe.springs:
        draw_arrow(screen, [int(s.p2.x), int(s.p2.y)], [int(s.p1.x), int(s.p1.y)])
        segments.append(((s.p2.x, s.p2.y), (s.p1.x, s.p1.y)))
        #segments.append())
    isect = poly_point_isect.isect_segments__naive(segments)
    text_to_screen(screen, "Total intersections: " + str(len(isect)), 500, 50)
    for pt in isect:
        pt = list(pt)
        pt[0] = int(pt[0])
        pt[1] = int(pt[1])
        pygame.draw.circle(screen, (255,0,0), pt, 2)


    pygame.display.flip()
    clock.tick(FPS)
