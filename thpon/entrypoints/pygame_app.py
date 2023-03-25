from thpon.domain import commands
# from allocation.service_layer.handlers import InvalidSku
from thpon import bootstrap

bus = bootstrap.bootstrap()

fid = 2
cmd = commands.FillInit(fid=fid)
bus.handle(cmd)
fld = bus.uow.fields.get(fid)

#
# https://github.com/furas/my-python-codes/tree/master/pygame/__template__/
#


import pygame

# === CONSTANS === (UPPER_CASE names)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

BLOCK_SIZE = 50

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

# --- objects ---


rects = []


x0, y0 = 20, 20    # just for example
dx, dy = 40, 40

rects = [[None for y in range(fld.rule.y_len)] for x in range(fld.rule.x_len)]

for y in range(fld.rule.y_len):
    for x in range(fld.rule.x_len):
        rect = pygame.Rect(x0 + x*dx, - y0-30 + SCREEN_HEIGHT - y*dy, 30,30)
        rects[x][y] = rect


def redraw():
    for y in range(fld.rule.y_len):
        for x in range(fld.rule.x_len):
            pygame.draw.rect(screen, fld.net[x][y].color, rects[x][y])

selected = None

# --- mainloop ---

clock = pygame.time.Clock()
is_running = True

while is_running:

    # --- events ---

    for event in pygame.event.get():

        # --- global events ---

        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for x, xrs in enumerate(rects):
                    for y, yr in enumerate(xrs):
                        if yr.collidepoint(event.pos):
                            selected = (x, y, yr.x, yr.y)
                            selected_offset_x = yr.x - event.pos[0]
                            selected_offset_y = yr.y - event.pos[1]
                            break

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if selected is not None:  # selected can be `0` so `is not None` is required
                    for x, xrs in enumerate(rects):
                        for y, yr in enumerate(xrs):
                            if x==selected[0] and y==selected[1]:
                                continue
                            if yr.collidepoint(event.pos):
                                target = (x, y, yr.x, yr.y)
                                cmd = commands.Swap(fid,
                                                    (selected[0], selected[1]),
                                                    (target[0], target[1]))
                                bus.handle(cmd)


                    rects[selected[0]][selected[1]].x = selected[2]
                    rects[selected[0]][selected[1]].y = selected[3]
                    redraw()

                selected = None

        elif event.type == pygame.MOUSEMOTION:
            if selected is not None:  # selected can be `0` so `is not None` is required
                # move object
                rects[selected[0]][selected[1]].x = event.pos[0] + selected_offset_x
                rects[selected[0]][selected[1]].y = event.pos[1] + selected_offset_y

        # --- objects events ---

        '''
       button.handle_event(event)
       '''

    # --- updates ---

    # empty

    # --- draws ---

    screen.fill(BLACK)

    '''
    button.draw(screen)    
    '''

    redraw()
    pygame.display.update()

    # --- FPS ---

    clock.tick(25)

# --- the end ---

pygame.quit()