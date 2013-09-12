__author__ = 'Kevin'

class Message(object):
    def __init__(self, type, obj):
        self.type = type
        self.obj = obj

    def __unicode__(self):
        return u"message: %s %s"%(self.type, self.obj)

    def __str__(self):
        return str(self.__unicode__())