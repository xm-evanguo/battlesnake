import json
import os
import random
import bottle
import numpy as np
import nextmove

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

    for head in data["you"]["body"][:1]:
        map[head["y"]][head["x"]] = 3
        head_xy = (head["x"], head["y"])

    for body in data["you"]["body"]:
        if np.equal(map[body["y"]][body["x"]], 0):
            map[body["y"]][body["x"]] = 2

    foods = []
    for food in data["board"]["food"]:
        map[food["y"]][food["x"]] = 1
        foods.append((food["x"], food["y"]))

    print(map)
    path = nextmove.shortest_path(map, head_xy, foods[0])
    print(path)
    '''
    if head_xy[0] is 0:
        directions.remove('left')
    elif head_xy[0] is map_width - 1:
        directions.remove('right')

    if head_xy[1] is 0:
        directions.remove('up')
    elif head_xy[1] is map_height - 1:
        directions.remove('down')

    direction = random.choice(directions)

    while(next_move_state(map, head_xy, direction) > 1):
        directions.remove(direction)
        direction = random.choice(directions)
    '''
    direction = nextmove.next_direction(map, head_xy, path[1])
    print(direction)
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
