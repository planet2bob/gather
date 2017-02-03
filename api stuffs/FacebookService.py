import fbchat
from Service import Service
import GatherMessage

class FBService(Service):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = fbchat.Client(username, password)
    
    def send_message(self, recipient, message):
        print(recipient)
        print(message)
        person = self.get_friend(recipient)
        sent = self.client.send(person.uid, message)
        if sent:
            return True
        return False
    
    def get_contacts(self):
        #I think I need tokens here, this is terrible, what am I doing?
        contact_list = []
        return contact_list
        
    def get_conversation(self, recipient):
        conversation = self.client.getThreadInfo(self.get_friend(recipient).uid, 0)
        revcontent = []
        for message in conversation:
            revcontent.append(message)
        content = []
        for i in range(len(revcontent)-1, -1, -1): #not smart but I had to do this to make fbchat happy
            content.append(revcontent[i])
        message_list = []
        for fbmsg in content:
            sender_recipient = self.get_Sender_Recipient(fbmsg, self.username, recipient)
            m = GatherMessage.GatherMessage(fbmsg.body, sender_recipient[0], sender_recipient[1])
            message_list.append(m)
        return message_list

    def get_Sender_Recipient(self, fbmsg, username, their_name):
        #only works for two people conversation
        #returns tuple (sender, recipient)
        if(fbmsg.author == self.get_friend(their_name).uid):
            return (their_name, username)
        return (username, their_name)
    
    def get_friend(self, their_name):
        return self.client.getUsers(their_name)[0]
