__author__ = 'Kevin'
import actors
from messages import Message
import time
import pygame
import common

class Universe(object):

    def __init__(self, conn, name):
        self.conn = conn
        self.name = name
        self.game_over = False
        self.i = 0
        self.name = None
        self.board = actors.Board()
        self.actors = []

    def handle_message(self, msg):
        if msg.type == common.QUIT:
            self.game_over = True
        if msg.type == common.IMPULSE:
            if pygame.K_LEFT in msg.obj:
                self.board.current_piece.impulse_left()
            if pygame.K_RIGHT in msg.obj:
                self.board.current_piece.impulse_right()
            if pygame.K_DOWN in msg.obj:
                self.board.current_piece.impulse_down()
            if pygame.K_UP in msg.obj:
                self.board.current_piece.impulse_up()
            if pygame.K_SPACE in msg.obj:
                self.board.current_piece.drop()

    def handle_tick(self, dt):
        self.board.handle_tick(dt)

    def play_loop(self):
        t0 = time.time()
        while not self.game_over:
            t1 = time.time()
            dt = t1 - t0
            t0 = t1
            if self.conn.poll():
                msg = self.conn.recv()
                self.handle_message(msg)
            self.handle_tick(dt)
            self.conn.send(Message(common.OBJECT_TREE, [self.board]))
        return True
