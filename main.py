import math
import pygame



SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

#BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

FPS = 120

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#screen_rect = screen.get_rect()

pygame.display.set_caption("web boi")


def text_to_screen(screen, text, x, y, size = 20,
    color = (255,255,255), font_type = 'arial'):

    text = str(text)
    font = pygame.font.SysFont(font_type, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))



class animal:
    def __init__(self, name):
        self.name = name

    def addDiet(self, diets):
        self.diets = diets
class rectclass:
    def __init__(self, a, b, c, d, val):
        self.rectang = pygame.rect.Rect(a, b, c, d)
        self.dragging = False
        self.pos = [a,b]
        self.val = val

def draw_arrow(screen, colour, start, end):
    pygame.draw.aaline(screen,colour,start,end,2)
    # rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
    # scale = 5
    # pygame.draw.polygon(screen, (0, 0, 0), ((end[0]+scale*math.sin(math.radians(rotation)), end[1]+scale*math.cos(math.radians(rotation))), (end[0]+scale*math.sin(math.radians(rotation-120)), end[1]+scale*math.cos(math.radians(rotation-120))), (end[0]+scale*math.sin(math.radians(rotation+120)), end[1]+scale*math.cos(math.radians(rotation+120)))))
    pygame.draw.circle(screen, (0,255,0), end, 3)  # Here <<<
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
    ("milkweed",),
    (),
    ("mosquito", "bulrush", "clam"),
    (),
    ("mosquito", "cattail")
]
print(len(diets) == len(allStuff))

allAnimals = {}
allObjects = {}
for i in range(len(allStuff)):
    allAnimals[allStuff[i]] = diets[i]
for name, diet in allAnimals.items():
    newAnimal = animal(name)
    newAnimal.addDiet(diet)
    #allObjects[name] = newAnimal
clock = pygame.time.Clock()
print(allAnimals)
print(allObjects)
allRects = []
counter = 0
print(allStuff)
for i in range(4):
    for y in range(5):
        print(5 * i + y)
        if counter < 17:
            counter += 1
            left = i * 120
            top = y * 120
            newRect = rectclass(left, top, 80, 80, allStuff[i*5 + y])
            allRects.append(newRect)
            #print(allStuff[i*4 + y])
            allObjects[allStuff[i*5 + y]] = newRect
        else:
            break
totalReceivers = {}

for i in range(len(allStuff)):
    x = allStuff[i]
    dietArray = diets[i]
    for y in dietArray:
        if y not in totalReceivers:
            totalReceivers[y] = [x]
        else:
            totalReceivers[y].append(x)

print(totalReceivers)
cool_gradient = 0
#print(allObjects)

running = True
current_dragged = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for rectangle in allRects:
                    if rectangle.rectang.collidepoint(event.pos):
                        rectangle.dragging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = rectangle.rectang.x - mouse_x
                        offset_y = rectangle.rectang.y - mouse_y
                        current_dragged = rectangle.val

                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for rectangle in allRects:
                    if rectangle.dragging:
                        rectangle.dragging = False
                        current_dragged = False
                        break

        elif event.type == pygame.MOUSEMOTION:
            if current_dragged:
                rectangle = allObjects[current_dragged]
                if rectangle.dragging:
                    mouse_x, mouse_y = event.pos
                    rectangle.rectang.x = mouse_x + offset_x
                    rectangle.pos[0] = mouse_x + offset_x
                    rectangle.rectang.y = mouse_y + offset_y
                    rectangle.pos[1] = mouse_y + offset_y
                    break

    # - updates (without draws) -

    # empty

    # - draws (without updates) -

    screen.fill((0,0,0))

    for rectangle in allRects:
        pygame.draw.rect(screen, (0,0,255), rectangle.rectang)
        text_to_screen(screen, rectangle.val, rectangle.pos[0], rectangle.pos[1])
        #print(allAnimals[rectangle.val])
    for prey, predators in allAnimals.items():
        p_x, p_y = allObjects[prey].pos

        if predators:


            for predator in predators:
                rectangle = allObjects[predator]
                draw_arrow(screen, (0, 200, 200), (rectangle.pos[0] + 40, rectangle.pos[1] + 40), (p_x + 20, p_y + 20))
    cool_gradient = (cool_gradient+1)% 255
    # for rectangle in allRects:
    #
    #     for diet in allAnimals[rectangle.val]:
    #
    #         prey_x, prey_y = allObjects[diet].pos
    #         draw_arrow(screen, (0,0,0),(prey_x+40, prey_y+40), (rectangle.pos[0] + 40, rectangle.pos[1] + 40))


    pygame.display.flip()

    # - constant game speed / FPS -

    clock.tick(FPS)

    # - end -

pygame.quit()
