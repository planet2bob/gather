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
        """
        send a skype message

        parameters:
        recipient, the skype username of the target
        message, the string of text to be messaged

        returns:
        no returns
        """
        
        channel = self.skype_class_object.contacts[recipient].chat
        channel.sendMsg(message)

    def get(self, target):
        """
        get past skype messages from a conversation

        parameters:
        target, the target contact that the conversation will be read from

        returns:
        a list of messages containing dictionaries
        the dictionary has the keys "sender" and "message" which contain the sender and message
        the list is in chronological order with index 0 being the latest
        """
    
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
        """
        finds the contacts associated with the account

        parameters:
        no parameters

        returns:
        a list of skype uernames that are on the user's account contacts
        """
        
        contacts = self.skype_class_object.contacts
        list_of_contacts = []
        
        for key in contacts:
            
            list_of_contacts.append(str(key.id))

        return list_of_contacts

def set_token():
    """identifies a text file to be the token file"""

    Skype_Connection_object = SkypeConnection()
    Skype_Connection_object.setTokenFile("token.txt")
    #This one's for you Kevin

def initialize_object(token,username,password):
    """creates the skype object"""
    
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
    """creates the module object"""

    skype_object = initialize_object(token,username,password)
    module_object = Skype_Class()
    module_object.skype_class_object = skype_object

    return module_object
