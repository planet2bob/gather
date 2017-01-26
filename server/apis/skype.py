from skpy import Skype
from skpy import SkypeConnection
import time, multiprocessing, requests

class SkypeProcess(multiprocessing.Process):
  
    def __init__(self, token, username, password):
        
        super(SkypeProcess, self).__init__()
        self.token = token

    def connect(self,token,username,password):

        if token == None:
        
            try:

                skype_object = Skype(username,password)

                return skype_object
            
            except requests.exceptions.ConnectionError:
        
                return None

        else:

            try:

                set_token()
                
                skype_object = Skype(tokenFile="skype_token.txt")
                
                return skype_object

            except requests.exceptions.ConnectionError:

                return None

class Skype_Class():

    skype_class_object = None

    def send(self, recipient, message):
        
        channel = self.skype_class_object.contacts[recipient].chat
        channel.sendMsg(message)

    def get(self, target):
    
        skype_chat = self.skype_class_object.contacts[target].chat
        target_id = skype_chat.id
        messages = self.skype_class_object.chats[target_id].getMsgs()

        list_of_messages = []
        
        for key in messages:

            sender = key.userId
            message = key.content

            if sender.find("live:") != -1:
                sender = sender[5:]
                
            list_of_messages.append({"sender":sender,"message":message})

        return list_of_messages

    def contacts(self):
        
        contacts = self.skype_class_object.contacts
        list_of_contacts = []
        
        for key in contacts:
            
            list_of_contacts.append(str(key.id))

        return list_of_contacts

def set_token():

        Skype_Connection_object = SkypeConnection()
        Skype_Connection_object.setTokenFile("token.txt")
        #This one's for you Kevin

def initialize_object(token,username,password):
    
    retry = True
    while retry == True:
        
        p = SkypeProcess(token,username,password)
        p.start()
        
        skype_object = p.connect(token,username,password)
        
        time.sleep(5)
        p.terminate()
        
        if skype_object == None:
            
            retry = True
            
        else:
            
            return skype_object

def login(token,username,password):

    skype_object = initialize_object(token,username,password)
    module_object = Skype_Class()
    module_object.skype_class_object = skype_object

    return module_object

def test():
    module_object = login(None,"gatherbois@gmail.com","Andrew_PAD_#_1")
    print(module_object.get("ptwob0"))

test()
