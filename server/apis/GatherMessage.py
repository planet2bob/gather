
class GatherMessage(object):
    '''This is a class that all messages should be passed as'''
    def __init__(self, body, sender, recipient):
        self.body = body
        self.sender = sender
        self.recipient = recipient

    def __str__(self):
        return str(self.sender) + '->' + str(self.body) + '->' + str(self.recipient)

    def __repr__(self):
        return self.__str__()
