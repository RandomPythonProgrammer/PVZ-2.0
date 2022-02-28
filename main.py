from utils.class_loader import classes, load_classes
from utils.asset_loader import load_sprites
from utils.display_utils import update_display
import pygame
import sys
import time


if __name__ == '__main__':

    window = pygame.display.set_mode((1280, 720), pygame.SCALED)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.MOUSEBUTTONUP])
    load_sprites()
    load_classes()

    world = classes['worlds']['day']()
    last_time = time.time()
    start_time = time.time()

    current_plant = classes['plants']['peashooter']

    while not world.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                for tile in world.tiles:
                    x, y = pygame.mouse.get_pos()
                    if tile.rect.collidepoint(x, y):
                        if current_plant.can_plant(tile, world):
                            world.plants.add(current_plant(tile.rect.x, tile.rect.y, tile, world))
                            break
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    world.paused = not world.paused
                    break
                if event.key == pygame.K_r:
                    world.spawn_zombie(classes['zombies']['basic'], False)
                    break
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        last_time = time.time()
        window.fill((0, 0, 0))
        world.render(window)
        update_display()
        if world.paused:
            continue
        world.update(time.time() - last_time)
