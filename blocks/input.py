__author__ = 'Kevin'
import pygame
from pygame import key

from messages import Message

class Inputter(object):

    def __init__(self, conn, name):
        pygame.init()
        self.conn = conn
        self.name = name
        pass

    def input_loop(self):
        while True:
            if self.conn.poll():
                self.conn.recv()
            pygame.event.pump()
