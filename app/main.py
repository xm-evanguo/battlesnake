import json
import os
import random
import bottle
import numpy as np
import nextmove
import detector
import othersnake

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#f75d4f"

    return start_response(color)

@bottle.post('/move')
def move():
    data = bottle.request.json
    #print(json.dumps(data))
    '''
    0 = empty
    1 = food
    2 = snake body
    3 = snake head
    7 = snake possible move
    8 = snake tail
    9 = two snake tail
    '''

    map_height = data["board"]["height"]
    map_width = data["board"]["width"]
    map = np.zeros((map_height, map_width), dtype = int)
    directions = ['up', 'down', 'left', 'right']
    my_id = data["you"]["id"]

    head_x = data["you"]["body"][0]["x"]
    head_y = data["you"]["body"][0]["y"]
    map[head_y][head_x] = 3
    head_xy = (head_x, head_y)
    my_length = len(data["you"]["body"])
    tail_list = othersnake.snakes_tail(data, map, my_id)

    for tail in tail_list:
        if np.equal(map[tail[1]][tail[0]], 8):
            map[tail[1]][tail[0]] = 9
        else:
            map[tail[1]][tail[0]] = 8

    for body in data["you"]["body"]:
        y = body["y"]
        x = body["x"]
        if np.equal(map[y][x], 0):
            map[y][x] = 2
            if (x,y) == othersnake.next_tail(data):
                break;

    if len(data["board"]["snakes"]) > 0:
        for item in data["board"]["snakes"]:
            x = item["body"][0]["x"]
            y = item["body"][0]["y"]
            map[y][x] = 3

        for item in data["board"]["snakes"]:
            for body in item["body"]:
                if np.equal(map[body["y"]][body["x"]], 0):
                    map[body["y"]][body["x"]] = 2

    foods = []
    for food in data["board"]["food"]:
        map[food["y"]][food["x"]] = 1
        foods.append((food["x"], food["y"]))

    simu_map = othersnake.map_simulation(data, map, my_length, my_id)

    print(simu_map)

    snakes_head_list = othersnake.snakes_head(data, simu_map, my_id)
    path = None
    if len(foods) > 0:
        nearFood = detector.findNearFood(foods, simu_map, head_xy, snakes_head_list)
        print("near food is : ", nearFood)

        for food in nearFood:
            path = nextmove.shortest_path(simu_map, head_xy, food)
            if path is not None:
                break
        print("path is ", path)

    my_next_tail = othersnake.next_tail(data)
    if path is None:
        bestMove = detector.bestMove(data, simu_map, head_xy, my_next_tail, map_height, map_width)
        print(bestMove)
        return move_response(bestMove)

    for food in nearFood[1:]:
        direction = nextmove.shortest_path(simu_map, head_xy, food)
        if direction is not None:
            break
    direction = nextmove.next_direction(simu_map, head_xy, path[1])
    print("direction is ", direction)

    bestMove = detector.bestMove(data, simu_map, head_xy, my_next_tail, map_height, map_width)
    print("bestmove is ", bestMove)

    if my_length < 15 or data["you"]["health"] < 40:
        if direction is not None:
            print("return direction")
            return move_response(direction)
    print("return bestMove")
    return move_response(bestMove)

@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
