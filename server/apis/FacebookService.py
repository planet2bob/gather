import fbchat
import GatherMessage

class FBService(Service):

    def _init_(self, username, password):
        self.username = username
        self.password = password
        self.client = fbchat.Client(username, password)
    
    def send_message(recipient, message):
        person = get_friend(recipient)
        sent = self.client.send(person.uid, message)
        if sent:
            return True
        return False
    
    def get_contacts(username):
        #I think I need tokens here, this is terrible, what am I doing?
        contact_list = []
        return contact_list
        
    def get_conversation(username, recipient):
        conversation = self.client.getThreadInfo(get_friend(recipient).uid, 0)
        content = []
        for message in convo:
            content.append(message.body)
        for fbmsg in content.reverse():
            sender_recipient = get_Sender_Recipient(fbmsg, username, recipient)
            m = GatherMessage.GatherMessage(fbmsg.body, sender_recipient[0], sender_recipient[1])
            message_list.append(m)
        return message_list

    def get_Sender_Recipient(fbmsg, username, their_name):
        #only works for two people conversation
        #returns tuple (sender, recipient)
        if(fbmsg.author == get_friend(their_name).uid):
            return (their_name, username)
        return (username, their_name)
    
    def get_friend(their_name):
        return self.client.getUsers(their_name)[0]
