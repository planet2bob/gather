class GatherMessage:

    def __init__(self, body, sender, recipient):
        self.body = body
        self.sender = sender
        self.recipient = recipient

    def display(self):
        print("\nBody: " + self.body + "\nSender: " + self.sender + "\nRecipient: " + self.recipient)

