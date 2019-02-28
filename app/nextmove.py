import collections

def next_move_state(map, head_xy, direction):
    switcher = {
        'left': (-1, 0),
        'right': (1, 0),
        'up': (0, -1),
        'down': (0, 1)
    }
    return map[head_xy[1] + switcher.get(direction)[1]][head_xy[0] + switcher.get(direction)[0]]

def next_direction(map, head_xy, move_xy):
    switcher = {
        (-1, 0): 'left',
        (1, 0): 'right',
        (0, -1): 'up',
        (0, 1): 'down'
    }
    return switcher.get(((move_xy[0] - head_xy[0]), (move_xy[1] - head_xy[1])))

def shortest_path(map, head_xy, goal):
    queue = collections.deque([[(head_xy[0], head_xy[1])]])
    seen = set([head_xy])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x,y) == goal:
            return path;
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < len(map) and 0 <= y2 < len(map) and map[y2][x2] < 2 and (x2,y2) not in seen:
                queue.append(path + [(x2,y2)])
                seen.add((x2,y2))
