import heapq

from .node import Node

from pkg.games.snake_game.constants import (
    X,
    Y,
)


# Object position to grid node converter
def obj_pos_to_node(game, position: tuple) -> Node:
    return game.grid[position[X]//game.grid_size][position[Y]//game.grid_size]


# Define a function to calculate the Manhattan distance heuristic
def heuristic(node, target):
    return abs(node.x - target.x) + abs(node.y - target.y)


# Define a function to get the neighboring nodes of a given node
def get_neighbors(game, node):
    neighbors = []
    if node.x > 0:
        neighbors.append(game.grid[node.x - 1][node.y])
    if node.x < game.grid_width - 1:
        neighbors.append(game.grid[node.x + 1][node.y])
    if node.y > 0:
        neighbors.append(game.grid[node.x][node.y - 1])
    if node.y < game.grid_height - 1:
        neighbors.append(game.grid[node.x][node.y + 1])
    return neighbors


# Define the A* pathfinding algorithm
def astar(game, start, end):
    # initilize the open and closed lists
    open_list = [start]
    closed_list = []

    while open_list:
        # Get the node with the lowest f value
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end:
            path = []
            while current_node:
                if current_node == start: break
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            return path[::-1]  # Reverse the path

        for neighbor in get_neighbors(game, current_node):
            if not neighbor.walkable or neighbor in closed_list:
                continue

            tentative_g = current_node.g + 1
            if neighbor not in open_list or tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, end)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node

                if neighbor not in open_list:
                    heapq.heappush(open_list, neighbor)

    return []  # No path found