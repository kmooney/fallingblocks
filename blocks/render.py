__author__ = 'Kevin'
from messages import Message
import common
import pygame
import threading
import time

ACTIVATORS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_a, pygame.K_s, pygame.K_d]

def setup_fonts():

    fonts = dict()
    fonts['regular'] = pygame.font.Font("resources/Verdana Bold.ttf",24)
    fonts['big'] = pygame.font.Font("resources/Verdana Bold.ttf", 32)
    fonts['small'] = pygame.font.Font("resources/Verdana Bold.ttf", 12)
    fonts['tiny'] = pygame.font.Font("resources/Verdana Bold.ttf", 10)
    return fonts

colors = [
    pygame.Color(0,0,128),
    pygame.Color(0,128,0),
    pygame.Color(128,0,0),
    pygame.Color(128,64,0),
    pygame.Color(64,64,128),
    pygame.Color(64,128,64),
    pygame.Color(255,128,64)

]

class Renderer(object):

    def __init__(self,conn, name):
        pygame.init()
        pygame.display.init()
        self.name = name
        self.conn = conn
        self.screen = pygame.display.set_mode((1200,900,), pygame.DOUBLEBUF, 32)
        pygame.font.init()
        self.fonts = setup_fonts()
        self.connection = None
        self.name = None
        self.object_tree = None
        self.game_over = False
        self.tile_height = 40
        self.tile_width = 40
        self.border_color = pygame.Color(150,150,200)



    def handle_messages(self):
        if self.conn.poll():
            msg = self.conn.recv()
            if msg.type == common.QUIT:
                self.game_over = True
            if msg.type == common.OBJECT_TREE:
                self.object_tree = msg.obj


    def draw_board(self, board):
        pos = board.get_geometry()[0]
        pygame.draw.rect(
            self.screen,
            self.border_color,
            pygame.Rect(
                pos[0], pos[1],
                board.width * self.tile_width, board.height * self.tile_height
            ),
            1
        )

    def draw_piece(self, board, piece):
        x,y,count = 0,0,0
        pos = piece.get_geometry()[0]
        board_pos = board.get_geometry()[0]

        for type in piece.tiles:
            # ugh - this is the binary representation of the count.
            # there must be a better way
            if count == 0:
                x,y = 0,0
            if count == 1:
                x,y = 0,1
            if count == 2:
                x,y = 1,0
            if count == 3:
                x,y = 1,1

            pygame.draw.rect(
                self.screen,
                colors[type],
                pygame.Rect(
                    board_pos[0]+pos[0]+self.tile_width*x,
                    board_pos[1]+pos[1]+self.tile_height*y,
                    self.tile_width, self.tile_height
                ),
                1
            )
            count += 1

    def render(self, boards):
        self.screen.fill((0,0,0))
        for board in boards:
            self.draw_board(board)
            self.draw_piece(board, board.current_piece)
        pygame.display.flip()

    def send_keystrokes(self):
        pygame.event.pump()
        keys = pygame.key.get_pressed()
        impulses = []

        for x in ACTIVATORS:
            if keys[x]:
                impulses.append(x)
        if keys[pygame.K_ESCAPE]:
            self.conn.send(Message(common.QUIT, "quit"))
            return False
        if impulses:
            msg = Message(common.IMPULSE, impulses)
            self.conn.send(msg)

    def render_loop(self):
        def rl():
            while not self.game_over:
                if self.object_tree:
                    self.render(self.object_tree)


        rl = threading.Thread(target=rl)
        rl.start()

        while not self.game_over:
            pygame.event.pump()
            self.handle_messages()
            if self.send_keystrokes() == False:
                self.handle_messages()
                return True
        rl.join()
        return True
