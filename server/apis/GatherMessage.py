
class GatherMessage(object):
    '''This is a class that all messages should be passed as'''
    def __init__(self, body, sender, recipient):
        self.body = body
        self.sender = sender
        self.recipient = recipient
