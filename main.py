from utils.class_loader import classes, load_classes
from utils.asset_loader import load_sprites
from utils.view_utils import ViewPort
from classes.tiles.tile import Tile
from utils.globals import global_variables
import traceback
import threading
import pygame
import os
import time


class KeyInterrupt(Exception):
    """Raised when an action is done to block other actions"""


def console():
    global current_item, team
    while True:
        try:
            command = input('$: ')
            words = command.split(' ')
            if words[0] == 'select':
                if words[1] != 'null':
                    current_item = classes[words[1]][words[2]]
                else:
                    current_item = None
            if words[0] == 'kill':
                while len([item for item in world.items if hasattr(item, 'on_death')]) > 0:
                    for item in world.items:
                        item.on_death()
            if words[0] == 'money':
                global_variables['money'] = int(words[1])
            if words[0] == 'team':
                team = int(words[1])
            if words[0] == 'stop':
                os._exit(0)
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':

    pygame.font.init()
    window = pygame.display.set_mode((1280, 720))
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.MOUSEBUTTONUP])
    load_sprites()
    load_classes()
    font = pygame.font.SysFont(None, 16)
    global_variables['money'] = 1000

    world = classes['world']['day'](ViewPort(0, 0, 1280, 720))
    last_time = time.time()
    start_time = time.time()
    console_thread = threading.Thread(target=console)
    console_thread.start()

    team = 1

    current_item = classes['farmitem']['atdmk1']

    while not world.game_over:

        if not world.paused:
            world.update(time.time() - last_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # kills all of the threads
                os._exit(0)
            try:
                if event.type == pygame.MOUSEBUTTONDOWN:

                    for item in world.items:
                        if hasattr(item, 'on_click'):
                            x_, y_ = pygame.mouse.get_pos()
                            x, y = world.view_port.unproject(x_, y_)
                            if item.rect.collidepoint(x, y):
                                if pygame.mouse.get_pressed()[0]:
                                    item.on_click(0)
                                elif pygame.mouse.get_pressed()[2]:
                                    item.on_click(1)
                                raise KeyInterrupt

                    if pygame.mouse.get_pressed()[0] and current_item is not None and \
                            (not hasattr(current_item, 'cost') or current_item.cost < global_variables['money']):
                        x_, y_ = pygame.mouse.get_pos()
                        x, y = world.view_port.unproject(x_, y_)
                        for tile in world.tiles:
                            if tile.rect.collidepoint(x, y):
                                if not hasattr(current_item, 'can_place') or current_item.can_place(tile, world):
                                    item = current_item(x, y, team, world)
                                    item.tile = tile
                                    world.items.append(item)
                                    if hasattr(current_item, 'cost'):
                                        global_variables['money'] -= current_item.cost
                                    raise KeyInterrupt

                    if pygame.mouse.get_pressed()[2] and pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        x_, y_ = pygame.mouse.get_pos()
                        x, y = world.view_port.unproject(x_, y_)
                        for item in world.items:
                            if hasattr(item, 'team') and item.team == team and item.rect.collidepoint(x, y):
                                world.items.remove(item)
                                raise KeyInterrupt
            except KeyInterrupt:
                pass
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    world.paused = not world.paused
                    break
                if event.key == pygame.K_r:
                    world.spawn_belligerent(classes['belligerent']['basic'], False)
                    break
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break
                if event.key == pygame.K_a:
                    world.view_port.x -= 100
                    break
                if event.key == pygame.K_d:
                    world.view_port.x += 100
                    break
        last_time = time.time()
        window.fill((0, 0, 0))
        world.render(window)
        window.blit(font.render(str(global_variables['money']), True, (255, 255, 0)), (0, 0))
        pygame.display.update()
