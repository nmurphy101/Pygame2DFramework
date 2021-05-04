import pygame
from itertools import permutations as perm

# pylint: disable=relative-beyond-top-level
from .astar import a_star_search, reconstruct_path
from ...entities.entity import Entity
# pylint: enable=relative-beyond-top-level


class Node:
    SIZE = 16
    BORDER = 0

    def __init__(self, pos, walkable):
        self.position = pos
        self.size = self.SIZE
        self.walkable = walkable

        self.rect = pygame.Rect(pos[0], pos[1], self.size, self.size)

    def set_size(self, val):
        self.size = val
        px, py = self.position
        self.rect = pygame.Rect(px, py, self.size, self.size)

    def draw(self, surface):
        col = pygame.Color('black') if self.walkable else pygame.Color('white')
        px, py = self.position
        sx, sy = (self.size,) * 2
        pygame.draw.rect(surface, col, self.rect.inflate(-self.BORDER, -self.BORDER))

    def get_neighbours(self):
        refx, refy = self.rect.center
        four_dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        eight_dirs = list(perm([0, 1, -1], 2)) + [(1, 1), (-1, -1)]

        neighs = []
        for d in four_dirs:
            dx, dy = d
            px, py = refx + (dx * Node.SIZE), refy + (dy * Node.SIZE)
            neighs.append((px, py))
        return neighs


class Graph(Entity):
    def __init__(self, base_game, screen, size, pos):
        self.name = "graph_"
        # Initilize parent init
        super().__init__(screen, size, self.name, base_game)
        self.alive = True
        self.killable = False
        self.graph_size = size
        self.position = pos
        self.nodes = self.make()

    def make(self):
        cx, cy = [gs // ns for ns, gs in zip((Node.SIZE, Node.SIZE), self.graph_size)]
        offx, offy = self.position

        res = []
        for x in range(cx + 2):
            for y in range(cy - 2):
                pos = offx + (x * Node.SIZE), offy + (y * Node.SIZE)
                n = Node(pos, True)
                res.append(n)
        return res

    def draw(self, surface, obj_dict):
        # Draw nodes
        for node in self.nodes:
            node.draw(surface)

    # def update(self, dt):
    #     for ag in self.agents:
    #         ag.update(dt)

    # def set_node_walkable(self, pos):
    #     for node in self.nodes:
    #         if node.rect.collidepoint(pos):
    #             node.walkable = not node.walkable


    def navigate(self, obj):
        # return if there is no target
        if not obj.target:
            return

        # calculate paths for all agents
        start = obj.rect.center
        goal = obj.target

        cf, cost = a_star_search(self, start, goal)
        try:
            path = reconstruct_path(cf, start, goal)
        except KeyError:
            return

        # Remove start position
        obj.set_path(path[2:])

    # These two last methods must be implemented for a_star to work
    def neighbors(self, pos):
        # determine the node at pos
        node = [n for n in self.nodes if n.rect.collidepoint(pos)][-1]

        # Get neighbouring nodes
        positions = node.get_neighbours()

        # Filter un-walkable positions
        res = []
        for pos in positions:
            for node in self.nodes:
                if node.rect.collidepoint(pos):
                    if node.walkable:
                        res.append(pos)
        return res

    def cost(self, p1, p2):
        return 10
