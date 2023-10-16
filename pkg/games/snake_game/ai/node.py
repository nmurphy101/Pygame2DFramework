# Node class
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0  # Cost from start node to this node
        self.h = 0  # Heuristic (estimated cost to goal)
        self.f = 0  # Total cost (f = g + h)
        self.parent = None
        self.walkable = True

    def __lt__(self, other):
        return self.f < other.f
