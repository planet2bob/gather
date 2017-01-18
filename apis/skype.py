from skpy import Skype
import time, multiprocessing, requests

class SkypeProcess(multiprocessing.Process):
  
    def __init__(self, username, password):
        
        super(SkypeProcess, self).__init__()
        self.username = username
        self.password = password
        self.birthTime = time.time()

    def age(self):
        
        return time.time() - self.birthTime

    def connect(self):
        
        try:
            
            skype_object = Skype(self.username, self.password)
            
            return skype_object
        
        except requests.exceptions.ConnectionError:
        
            return None

def initialize_object(username,password):
    
    retry = True
    while retry == True:
        
        username,password = get_login_info()
        
        p = SkypeProcess(username,password)
        p.start()
        
        skype_object = p.connect()
        
        time.sleep(5)
        p.terminate()
        
        if skype_object == None:
            
            retry = True
            
        else:
            
            return skype_object

def get_skype_contacts(skype_object):
    
    contacts = skype_object.contacts
    list_of_contacts = []
    
    for key in contacts:
        
        list_of_contacts.append(str(key.id))

    return list_of_contacts

def send_message(skype_object, recipient, message):

    channel = skype_object.contacts[recipient].chat
    channel.sendMsg(message)

def get_message(skype_object, target):
    
    skype_chat = skype_object.contacts[target].chat
    target_id = skype_chat.id
    messages = skype_object.chats[target_id].getMsgs()

    list_of_messages = []
    
    for key in messages:
        
        if key.userId == target:
            
            list_of_messages.append(str(key.content))

    return list_of_messages
