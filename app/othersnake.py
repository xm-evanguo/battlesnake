def snakes_head(data, map):
    snakes_info = []
    for snakes in data["snakes"][1:]:
        snakes_info.append((len(snakes["body"]), snakes["body"][0]["x"], snakes["body"][0]["y"]))
    return snakes_info

def map_simulation(map, my_length, snakes_info):
    simulation_map = map
    for head in snakes_info:
        x = head[1]
        y = head[2]
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < len(map) and 0 <= y2 < len(map) and map[y2][x2] < 2 and head[0] >= my_length:
                simulation_map[y2][x2] = 2
    return simulation_map
