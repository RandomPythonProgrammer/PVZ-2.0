from utils.class_loader import classes, load_classes
from utils.asset_loader import load_sprites
from utils.input_utils import get_cancelled, set_cancelled, events, get_events
from utils.view_utils import ViewPort
import pygame
import sys
import time


if __name__ == '__main__':

    window = pygame.display.set_mode((1280, 720))
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.MOUSEBUTTONUP])
    load_sprites()
    load_classes()

    world = classes['world']['day'](ViewPort(0, 0, 1280, 720))
    last_time = time.time()
    start_time = time.time()

    current_item = classes['farmitem']['peashooter']

    while not world.game_over:
        set_cancelled(False)
        get_events()
        if not world.paused:
            world.update(time.time() - last_time)
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP and not get_cancelled():
                for tile in world.tiles:
                    x_, y_ = pygame.mouse.get_pos()
                    x, y = world.view_port.unproject(x_, y_)
                    if tile.rect.collidepoint(x, y):
                        if current_item.can_place(tile, world):
                            world.farm_items.append(current_item(tile.rect.x, tile.rect.y, tile, 1, world))
                            set_cancelled(True)
                            break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    world.paused = not world.paused
                    break
                if event.key == pygame.K_r:
                    world.spawn_belligerent(classes['belligerent']['basic'], False)
                    break
                if event.key == pygame.K_e:
                    world.spawn_sun()
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
        pygame.display.update()
