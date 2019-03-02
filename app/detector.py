import nextmove

def bestMove(map, head_xy, tail_xy, map_height, map_width):
    # 1.no wall, 2.more space, 3.near food
    index = [[0,'up'],[0,'down'],[0,'left'],[0,'right']]
    x = head_xy[0]
    y = head_xy[1]

    for i in range(y-1, -1, -1): #check up
        if map[i][x] < 2:
            index[0][0] += 1
        else:
            break
    for i in range(y+1, map_height): #check down
        if map[i][x] < 2:
            index[1][0] += 1
        else:
            break
    for i in range(x-1, -1, -1): #check left
        if map[y][i] < 2:
            index[2][0] += 1
        else:
            break
    for i in range(x+1, map_width): #check right
        if map[y][i] < 2:
            index[3][0] += 1
        else:
            break
    print(x,y)

    path = nextmove.shortest_path(map, head_xy, tail_xy)
    if path is None:
        if 1 <= y < map_height and x < map_width and map[y-1][x] < 2:
            index[0][0] -= 1
        if y+1 < map_height and x < map_width and map[y+1][x] < 2:
            index[1][0] -= 1
        if y < map_height and 1 <= x < map_width and map[y][x-1] < 2:
            index[2][0] -= 1
        if y < map_height and x+1 < map_width and map[y][x+1] < 2:
            index[3][0] -= 1

    if y == 0:
        index[0][0] -= 10000
    if y + 1 >= map_height:
        index[1][0] -= 10000
    if x == 0:
        index[2][0] -= 10000
    if x + 1 >= map_width:
        index[3][0] -= 10000

    if y < map_height and x < map_width and map[y-1][x-1] == 2:
            index[0][0] -= 2
            index[2][0] -= 2

    if y < map_height and x+1 < map_width and map[y-1][x+1] == 2:
            index[0][0] -= 2
            index[3][0] -= 2

    if y+1 < map_height and x < map_width and map[y+1][x-1] == 2:
            index[1][0] -= 2
            index[2][0] -= 2

    if y+1 < map_height and x+1 < map_width and map[y+1][x+1] == 2:
            index[1][0] -= 2
            index[3][0] -= 2

    if y < map_height and x < map_width and map[y-1][x] >= 2:
        if map[y-1][x] == 9:
            index[0][0] -= 100
        else:
            index[0][0] -= 1000

    if y+1 < map_height and x < map_width and map[y+1][x] >= 2:
        if map[y+1][x] == 9:
            index[1][0] -= 100
        else:
            index[1][0] -= 1000

    if y < map_height and x < map_width and map[y][x-1] >= 2:
        if map[y][x-1] == 9:
            index[2][0] -= 100
        else:
            index[2][0] -= 1000

    if y < map_height and x+1 < map_width and map[y][x+1] >= 2:
        if map[y][x+1] == 9:
            index[3][0] -= 100
        else:
            index[3][0] -= 1000

    print(index)
    return max(index)[1]


def findNearFood(foods, map, head_xy, snakes):

    foodDistanceSorted = []
    foodDistance = {}

    for i in range(0, len(foods)):
        distance = abs(head_xy[0] - foods[i][0]) + abs(head_xy[1] - foods[i][1])
        if distance in foodDistance:
            foodDistance[distance].append(foods[i])
        else:
            foodDistance.update({distance:[foods[i]]})

    for i in sorted(foodDistance):
        foodDistanceSorted += foodDistance[i]

    #print(foodDistance)
    #print(foodDistanceSorted)

    if len(foodDistanceSorted) > 0:
        bestFood = foodDistanceSorted[0]
    else:
        return None

    """
    for distance in foodDistanceSorted:
        check = 0
        for xy in foodDistanceSorted[distance]:
            for snake in snakes:
                otherDis = abs(snake[0] - xy[0]) + abs(snake[1] - xy[1])
                if otherDis < distance:
                    check = 1
            if check == 0:
                bestFood = xy
                break
        if check == 1:
            break
            """

    for xy in foodDistanceSorted:
        check = 0
        for snake in snakes:
            otherDis = abs(snake[0] - xy[0]) + abs(snake[1] - xy[1])
            if otherDis < distance:
                check = 1
        if check == 0:
            bestFood = xy
            break

    bestFood_list = [bestFood]
    #print(bestFood)

    for item in foodDistanceSorted:
        if item not in bestFood_list:
            bestFood_list.append(item)

    return bestFood_list
