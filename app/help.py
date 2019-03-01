def bestMove(map, head_xy, direction, map_height, map_width):
    # 1.no wall, 2.more space, 3.near food
    index = [0,0,0,0]
    x = head_xy[0]
    y = head_xy[1]
    print(x,y, map_height,map_width)

    for i in range(y-1, -1, -1): #check up
        if map[i][x] < 2:
            index[0] += 1
        else:
            break
    for i in range(y+1, map_height): #check down
        if map[i][x] < 2:
            index[1] += 1
        else:
            break
    for i in range(x-1, -1, -1): #check left
        if map[y][i] < 2:
            index[2] += 1
        else:
            break
    for i in range(x+1, map_width): #check right
        if map[y][i] < 2:
            index[3] += 1
        else:
            break

    if map[y-1][x-1] >= 2:
        index[0] -= 1
        index[2] -= 1

    if map[y-1][x+1] >= 2:
        index[0] -= 1
        index[3] -= 1

    if map[y+1][x-1] >= 2:
        index[1] -= 1
        index[2] -= 1

    if map[y+1][x+1] >= 2:
        index[1] -= 1
        index[3] -= 1

    return index


def findNearFood(foods, map, head_xy, snakes):

    foodDistance = {}

    for i in range(0, len(foods)):
        distance = abs(head_xy[0] - foods[i][0]) + abs(head_xy[1] - foods[i][1])
        if distance in foodDistance:
            foodDistance[distance].append(foods[i])
        else:
            foodDistance.update({distance:[foods[i]]})

    default = foodDistance.values[0][0]

    for distance in foodDistance:
        check = 0
        for xy in foodDistance[distance]:
            for snake in snakes:
                otherDis = abs(snake[0] - xy[0]) + abs(snake[1] - xy[1])
                if otherDis < distance:
                    check = 1
            if check == 0:
                return xy

    return default
