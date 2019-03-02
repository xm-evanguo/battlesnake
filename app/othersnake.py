import numpy as np

def snakes_length(data, map):
    length = []
    for snakes in data["board"]["snakes"][1:]:
        length.append(len(snakes["body"]))
    return length

def snakes_head(data, map):
    head_list = []
    for snakes in data["board"]["snakes"][1:]:
        head_list.append((snakes["body"][0]["x"], snakes["body"][0]["y"]))
    return head_list

def snakes_tail(data, map):
    tail_list = []
    for snakes in data["board"]["snakes"][1:]:
        tail_list.append((snakes["body"][len(snakes["body"]) - 1]["x"], snakes["body"][len(snakes["body"]) - 1]["y"]))
    return tail_list

def snakes_num(data):
    return len(data["board"]["snakes"])

def map_simulation(data, map, my_length):
    length_list = snakes_length(data, map)
    head_list = snakes_head(data, map)
    tail_list = snakes_tail(data, map)
    n_snakes = snakes_num(data)
    return simu_map(map, my_length, length_list, head_list, tail_list, n_snakes)

def simu_map(map, my_length, length_list, head_list, tail_list, n_snakes):
    simulation_map = map
    for i in range(n_snakes-1):
        x = head_list[i][0]
        y = head_list[i][1]
        if length_list[i] >= my_length:
            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                if 0 <= x2 < len(map) and 0 <= y2 < len(map) and map[y2][x2] < 2:
                    simulation_map[y2][x2] = 3

        x = tail_list[i][0]
        y = tail_list[i][1]
        if not np.equal(map[y][x], 4):
            simulation_map[y][x] = 0

    return simulation_map
