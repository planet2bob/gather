from GatherMessage import GatherMessage
from GatherService import GatherService
from skpy import Skype, SkypeConnection, SkypeChats
import time, multiprocessing, requests
from datetime import datetime

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
        try:
            channel = self.skype_object.contacts[recipient].chat
            channel.sendMsg(message)
            return True
        
        except:
            return False

    def get_messages(self,target):
        chats_object = SkypeChats(self.skype_object)
        messages = chats_object.recent()
        single_chat = messages["8:" + target]
        results = []
        for message in single_chat.getMsgs():
            content = message.content
            sender = message.userId
            recipient = message.chatId
            time = datetime.strptime(str(message.time),"%Y-%m-%d %H:%M:%S.%f")
            if "8:" + sender == recipient:
                sender = self.username
            results.append(GatherMessage(str(content), str(sender), str(recipient), time))
        return results

def login(username,password):
    return SkypeService(None, username, password)
