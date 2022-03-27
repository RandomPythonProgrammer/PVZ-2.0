from utils.class_loader import classes, load_classes
from utils.asset_loader import load_sprites
from utils.view_utils import ViewPort
from classes.objects.object import Object
import traceback
import threading
import pygame
import os
import time
import pickle
import socket
from utils.event_utils import *

userdata = {}


def click(item: object):
    x_, y_ = pygame.mouse.get_pos()
    x, y = world.view_port.unproject(x_, y_)
    if item.rect.collidepoint(x, y):
        if pygame.mouse.get_pressed()[0]:
            item.on_click(0)
        elif pygame.mouse.get_pressed()[2]:
            item.on_click(1)
        raise KeyInterrupt


class KeyInterrupt(Exception):
    """Raised when an action is done to block other actions"""


if __name__ == '__main__':

    pygame.font.init()
    window = pygame.display.set_mode((1280, 720))
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.MOUSEBUTTONUP])
    load_sprites()
    load_classes()
    font = pygame.font.SysFont(None, 16)

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(pickle.dumps(PlayerConnectEvent(1)), ('127.0.0.1', 2222))

    world = classes['world']['day'](ViewPort(0, 0, 1280, 720))
    last_time = time.time()
    start_time = time.time()

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

                    if pygame.mouse.get_pressed()[2] and pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        x_, y_ = pygame.mouse.get_pos()
                        x, y = world.view_port.unproject(x_, y_)
                        for item in world.items:
                            if hasattr(item, 'team') and item.team == userdata['team'] and item.rect.collidepoint(x, y):
                                item.on_death()
                                raise KeyInterrupt

                    for item in world.get_items(Object):
                        if hasattr(item, 'on_click') and not item.background:
                            click(item)
                    for item in world.items:
                        if hasattr(item, 'on_click') and not hasattr(item, 'background'):
                            click(item)
                    for item in world.get_items(Object):
                        if hasattr(item, 'on_click') and item.background:
                            click(item)

                    if pygame.mouse.get_pressed()[0] and current_item is not None and \
                            (not hasattr(current_item, 'cost') or current_item.cost < userdata['money']):
                        x_, y_ = pygame.mouse.get_pos()
                        x, y = world.view_port.unproject(x_, y_)
                        for tile in world.tiles:
                            if tile.rect.collidepoint(x, y):
                                #send message to place
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
        window.blit(font.render(str(userdata['money']), True, (255, 255, 0)), (0, 0))
        pygame.display.update()
