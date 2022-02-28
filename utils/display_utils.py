import pygame

update_queue: pygame.rect = []


def update_display():
    pygame.display.update(update_queue)
    update_queue.clear()
