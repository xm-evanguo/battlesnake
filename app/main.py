import json
import os
import random
import bottle
import numpy as np
import nextmove
import help
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

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    #print(json.dumps(data))
    map_height = data["board"]["height"]
    map_width = data["board"]["width"]
    map = np.zeros((map_height, map_width), dtype = int)
    directions = ['up', 'down', 'left', 'right']
    my_id = data["you"]["id"]

    head_x = data["you"]["body"][0]["x"]
    head_y = data["you"]["body"][0]["y"]
    map[head_y][head_x] = 3
    head_xy = (head_x, head_y)

    for body in data["you"]["body"]:
        if np.equal(map[body["y"]][body["x"]], 0):
            map[body["y"]][body["x"]] = 2

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

    print(map)
    """
    for food in foods:
        path = nextmove.shortest_path(map, head_xy, food)
        if path is not None:
            break
    """

    snakes = othersnake.snakes_head(data, map)
    nearFood = help.findNearFood(foods, map, head_xy, snakes)
    print(nearFood)

    path = nextmove.shortest_path(map, head_xy, nearFood)
    print(path)

    direction = nextmove.next_direction(map, head_xy, path[1])
    print(direction)

    bestMove = help.bestMove(map, head_xy, direction, map_height, map_width)
    print(bestMove)

    if data["you"]["health"] > 60:
        return move_response(bestMove)
    else:
        return move_response(direction)

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
