from GatherMessage import GatherMessage
from GatherService import GatherService
from skpy import Skype, SkypeConnection, SkypeChats
import time, multiprocessing, requests

class SkypeProcess(multiprocessing.Process):
  
    def __init__(self, token, username, password):
        
        super(SkypeProcess, self).__init__()
        self.token = token

    def connect(self, token, username, password):

        if token == None:
            try:
                skype_object = Skype(username,password)
                return skype_object
            
            except requests.exceptions.ConnectionError:
                return None

        else:
            raise Exception("Need to impliment tokens in Skype")

class SkypeService(GatherService):

    def __init__(self,token,username,password):
        self.username = username
        p = SkypeProcess(token,username,password)
        p.start()
        self.skype_object = p.connect(token,username,password)
        time.sleep(5)
        p.terminate()

        if self.skype_object == None:
            raise Exception("Skype Object failed to connect")

    def get_contacts(self):
        contacts = self.skype_object.contacts
        list_of_contacts = []
        
        for key in contacts:
            
            list_of_contacts.append(str(key.id))

        return list_of_contacts

    def send_message(self, recipient, message):
        channel = self.skype_object.contacts[recipient].chat
        channel.sendMsg(message)

    def get_messages(self,target):
        chats_object = SkypeChats(self.skype_object)
        messages = chats_object.recent()
        single_chat = messages["8:" + target]
        results = []
        for message in single_chat.getMsgs():
            content = message.content
            sender = message.userId
            recipient = message.chatId
            if "8:" + sender == recipient:
                sender = self.username
            print type(sender)
            print type(recipient)
            print type(content)
            results.append(GatherMessage(str(content), str(sender), str(recipient)))
        for r in results:
            print r
        return results

def login(username,password):
    return SkypeService(None, username, password)

ss = login("gatherbois@gmail.com", "Andrew_PAD_#_1")
print(ss.get_contacts())
print ss.get_messages("live:maxlouiesun")
