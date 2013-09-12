__author__ = 'Kevin'

class Routing(object):

    def __init__(self, name):
        self.name = name
        self.routing_table = dict()
        self.message_table = dict()
        self.shutdown = False
        self.flush_counter = 1

    def add_connection(self, connection, name):
        """
        Add a named connection to the routing table.
        """
        self.routing_table[name]=connection

    def register(self, name, message_type):
        """
        Register a named entity with a message type.  When a message is
        received, its type is checked, then it is sent down a different pipe.
        """
        if message_type not in self.message_table:
            self.message_table[message_type] = []
        self.message_table[message_type].append(name)
        print self.message_table


    def routing_loop(self):
        while True:
            for name, conn in self.routing_table.iteritems():
                if conn.poll():
                    msg = conn.recv()
                    addressees = self.message_table.get(msg.type, [])
                    for who in addressees:
                        sendto = self.routing_table.get(who, None)
                        if sendto and not self.shutdown:
                            sendto.send(msg)
                    if msg.type == 'quit':
                        self.shutdown = True
                elif self.shutdown and self.flush_counter == 0:
                    return True
                elif self.shutdown and self.flush_counter != 0:
                    self.flush_counter -= 1
