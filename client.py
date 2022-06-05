import json
import random
import numpy

from utils.class_loader import classes, load_classes
from utils.asset_loader import load_sprites
from utils.view_utils import ViewPort
from classes.objects.object import Object
from classes.belligerents.belligerent import Belligerent
from utils.globals import global_variables
import traceback
import threading
import pygame
import os
import time


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

    with open('levels/day/1.json', 'r') as file:
        level_data = json.load(file)

    world = classes['world'][level_data['world']](ViewPort(0, 0, 1280, 720))
    last_time = time.time()
    start_time = time.time()
    console_thread = threading.Thread(target=console)
    console_thread.start()

    team = 1

    current_item = classes['farmitem']['atdmk1']

    world.belligerent_queue = level_data['belligerents']['roam']
    last_spawn_time = time.time()

    while not world.game_over:

        if not world.paused:
            world.update(time.time() - last_time)
            if len(world.belligerent_queue.keys()) == 0:
                if len(world.get_items(Belligerent)) == 0:
                    if not world.is_wave and world.current_wave < len(level_data['belligerents']['waves']):
                        world.on_wave()
                        world.belligerent_queue = level_data['belligerents']['waves'][world.current_wave]
                        world.current_wave += 1
                        world.is_wave = True
                    else:
                        world.is_wave = False
                        world.belligerent_queue = level_data['belligerents']['roam']
            elif time.time() - last_spawn_time > numpy.random.normal(loc=1, scale=0.2) * (level_data['wave_spawn_delay'] if world.is_wave else level_data['spawn_delay']):
                belligerent = random.choice(list(world.belligerent_queue.keys()))
                world.belligerent_queue[belligerent] -= 1
                if world.belligerent_queue[belligerent] <= 0:
                    world.belligerent_queue.pop(belligerent)
                world.spawn_belligerent(classes['belligerent'][belligerent], world.is_wave)
                last_spawn_time = time.time()

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
                            if hasattr(item, 'team') and item.team == team and item.rect.collidepoint(x, y):
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
