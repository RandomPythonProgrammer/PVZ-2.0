from utils.class_loader import classes, load_classes
from utils.view_utils import ViewPort
import traceback
import threading
from utils.event_utils import *
import os
import time
import pickle
import socket

port = input("enter the port: ")
userdata = {}


def console():
    global current_item, team
    while True:
        try:
            command = input('$: ')
            words = command.split(' ')
            if words[0] == 'kill':
                while len([item for item in world.items if hasattr(item, 'on_death')]) > 0:
                    for item in world.items:
                        item.on_death()
            if words[0] == 'stop':
                server.close()
                os._exit(0)
        except Exception:
            traceback.print_exc()


def event_handler():
    global events
    data, origin = server.recvfrom(1024)
    events.append(pickle.loads(data))


if __name__ == '__main__':
    events = []
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', port))

    while len(userdata.keys()) < 1:
        data, origin = server.recvfrom(1024)
        data = pickle.loads(data)
        if isinstance(data, PlayerConnectEvent) and data.team not in userdata.keys():
            userdata[data.team] = {'money': 1500}

    load_classes()
    world = classes['world']['day'](ViewPort(0, 0, 1280, 720))
    last_time = time.time()
    start_time = time.time()
    console_thread = threading.Thread(target=console)
    console_thread.start()

    event_handler_thread = threading.Thread(target=event_handler)
    event_handler_thread.start()

    while not world.game_over:

        if not world.paused:
            world.update(time.time() - last_time)
        for event in events:
            if isinstance(event, PlayerDisconnectEvent):
                server.close()
                os._exit(1)
            if isinstance(event, PlaceEvent):
                tile = event.tile
                placed = event.placed
                if userdata[event.team]['money'] >= placed.cost:
                    x, y = event.x, event.y
                    if not hasattr(placed, 'can_place') or placed.can_place(tile, world):
                        item = placed(x, y, team, world)
                        item.tile = tile
                        world.items.append(item)
                        if hasattr(placed, 'cost'):
                            userdata[event.team]['money'] -= current_item.cost

        last_time = time.time()
