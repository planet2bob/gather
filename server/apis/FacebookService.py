import fbchat
from GatherService import GatherService
import GatherMessage

class FacebookService(GatherService):
    
    def __init__(self, username, password):
        self.username = username
        self.client = fbchat.Client(username, password)
        
    def get_contacts(self):
        '''Returns all contacts from service'''
        #I need tokens for this, Kevin!!  >________<
        raise NotImplementedError("Must implement get_contacts")
    
    def get_messages(self, recipient):
        '''Returns GatherMessages given a contact'''
        conversation = self.client.getThreadInfo(self.get_friend(recipient).uid, 0)
        revcontent = []
        for message in conversation:
            revcontent.append(message)
        content = []
        for i in range(len(revcontent)-1, -1, -1): #not smart but I had to do this to make fbchat happy
            content.append(revcontent[i])
        message_list = []
        for fbmsg in content:
            message_list.append(self.convert_message(fbmsg, recipient))
        return message_list
    
    def convert_message(self, fbmsg,recipient):
        sender_recipient = self.get_Sender_Recipient(fbmsg, self.username, recipient)
        return GatherMessage.GatherMessage(str(fbmsg.body), sender_recipient[0], sender_recipient[1], fbmsg.timestamp) #Note: I'm currently assuming we're using timestamp for GatherMessage's time field...
        
    def get_Sender_Recipient(self, fbmsg, username, their_name):
        #only works for two people conversation, returns tuple(sender, recipient)
        if(fbmsg.author == self.get_friend(their_name).uid):
            return (their_name, username)
        return (username, their_name)
            
    def send_message(self, recipient, message):
        '''Sends (string) message to recipient'''
        person = self.get_friend(recipient)
        sent = self.client.send(person.uid, message)
        if sent:
            return True
        return False
    
    def get_friend(self, their_name):
        return self.client.getUsers(their_name)[0]

