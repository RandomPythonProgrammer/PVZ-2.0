from utils.class_loader import classes, load_classes
from utils.asset_loader import sprites, load_sprites
import pygame
import sys
import time


if __name__ == '__main__':

    window = pygame.display.set_mode((1280, 720), pygame.SCALED)
    load_sprites()
    load_classes()

    world = classes['worlds']['day']()
    last_time = time.time()
    start_time = time.time()

    current_plant = classes['plants']['peashooter']
    world.zombies.add(classes['zombies']['basic'](500, 0, world))

    while not world.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                for tile in world.tiles:
                    if tile.rect.collidepoint(pygame.mouse.get_pos()):
                        if current_plant.can_plant(tile, world):
                            world.plants.add(current_plant(tile.rect.x, tile.rect.y, tile, world))
        world.update(time.time() - last_time)
        last_time = time.time()
        window.fill((0, 0, 0))
        world.render(window)
        pygame.display.update()
