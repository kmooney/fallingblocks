__author__ = 'Kevin'
from exceptions import NotImplementedError
import random


TILE_TYPES = [
    1,2,3,4,5,6
]

def near(a, b, c = 0.15):
    if abs(a-b) < c:
        return True
    return False

class Moveable(object):
    def __init__(self):
        self.pos = (0.0,0.0,)
        self.velocity = (0.0,0.0,)
        self.acceleration = (0.0,0.0,)
        self.drag = (1, 1)

    def next_position(self, dt):
        self.pos = (
            self.pos[0] + self.velocity[0]*dt,
            self.pos[1] + self.velocity[1]*dt
        )

    def next_velocity(self, dt):
        x, y = self.velocity
        ax, ay = self.acceleration
        drx, dry = self.drag
        self.acceleration = (0,0)

        x += ax * dt
        y += ay * dt

        if near(x,0): x = 0
        if near(y, 0): y= 0

        if x > 0:
            x -= (drx * dt)
        if x < 0:
            x += (drx * dt)
        if y > 0:
            y -= (dry * dt)
        if y < 0:
            y += (dry * dt)

        self.velocity = (x, y)

    def handle_tick(self,dt):
        raise NotImplementedError(
            "You must implement 'handle_tick' in a subclass!"
        )

    def get_geometry(self):
        raise NotImplementedError(
            "You must implement 'get_geometry' in a subclass!"
        )

class Board(Moveable):
    width = 10
    height = 20

    def __init__(self):
        super(Board, self).__init__()
        self.size = (10,20,)
        self.tiles = []
        self.board = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
        ]
        self.current_piece = ComposedTile(self)


    def get_geometry(self):
        return (400,20), 'board'

    def handle_tick(self, dt):
        if self.current_piece == None:
            self.current_piece = ComposedTile(self)
        for tile in self.tiles:
            tile.handle_tick(dt)
        self.current_piece.handle_tick(dt)


class Tile(Moveable):

    def __init__(self, tile_type):
        super(Tile, self).__init__()
        self.type = tile_type

    def handle_tick(self, dt):
        # figure out if I should remove myself.
        pass

    def get_geometry(self):
        return self.pos, 'tile'

class ComposedTile(Moveable):

    def __init__(self,board):
        super(ComposedTile,self).__init__()
        self.board = board
        self.tiles = []
        for x in xrange(0,4):
            self.tiles.append(random.choice(TILE_TYPES))

    def next_velocity(self, dt):
        super(ComposedTile, self).next_velocity(dt)


    def handle_tick(self, dt):
        # drop me down.  Figure out if my tiles should decompose.
        #self.impulse_down()
        self.next_position(dt)
        self.next_velocity(dt)

    def impulse_right(self):
        x,y = self.acceleration
        x += 10000
        self.acceleration = x,y

    def impulse_left(self):
        x,y = self.acceleration
        x += -10000
        self.acceleration = x,y

    def impulse_down(self):
        x,y = self.acceleration
        y += 10000
        self.acceleration = x,y

    def impulse_up(self):
        x,y = self.acceleration
        y += -10000
        self.acceleration = x,y

    def drop(self):
        # loop y position till we collide with something all in one frame!
        pass

    def get_geometry(self):
        return self.pos, 'compose_tile'
