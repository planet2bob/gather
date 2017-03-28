class GatherMessage(object):
    '''This is a class that all messages should be passed as'''
    def __init__(self, body, sender, recipient,time):
        self.body = body
        self.sender = sender
        self.recipient = recipient
        self.time = time

    def __str__(self):
        return str(self.sender) + '->' + str(self.body) + '->' + str(self.recipient) + '->' + str(self.time)

    def __repr__(self):
        return self.__str__()
