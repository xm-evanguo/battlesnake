def snakes_length(data, map):
    snakes_length = []
    for snakes in data["snakes"][1:]:
        snake_length.append(len(snakes["body"]))
    return snakes_length

def snakes_head(data, map):
    snakes_body = []
    for snakes in data["snakes"][1:]:
        snakes_body.append((snakes["body"][0]["x"], snakes["body"][0]["y"]))
    return snakes_body

def snakes_tail(data, map):
    snakes_tail = []
    for snakes in data["snakes"][1:]:
        snakes_tail.append((snakes["body"][len(snakes["body"]) - 1]["x"], snakes["body"][len(snakes["body"]) - 1]["y"]))
    return snakes_tail

def map_simulation(map, my_length, snakes_info):
    simulation_map = map
    for head in snakes_info:
        x = head[1]
        y = head[2]
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < len(map) and 0 <= y2 < len(map) and map[y2][x2] < 2 and head[0] >= my_length:
                simulation_map[y2][x2] = 2
    return simulation_map
