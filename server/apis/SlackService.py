from slackclient import SlackClient
from GatherMessage import GatherMessage
from GatherService import GatherService
from datetime import datetime

class SlackService(GatherService):

    def __init__(self,token,username,password):
        self.username = username
        self.password = password
        self.token = token

        self.slack_object = SlackClient(token)

    def send_message(self, recipient, message):
        users = self.slack_object.api_call(
            "users.list"
            )
        
        members = users["members"]

        counter = 0
        while counter < len(members):
            member = members[counter]
            if member["name"] == recipient:
                
                recipient_id = member["id"]
                message_channel_object = self.slack_object.api_call(
                    "im.open",
                    user = recipient_id,
                    return_im = False
                    )
                channel = message_channel_object["channel"]
                channel_id = channel["id"]

                try:
                    self.slack_object.api_call(
                    "chat.postMessage",
                    channel=channel_id,
                    text=message
                    )
                    return True
                
                except:
                    return False
                
            counter = counter + 1

        return False

    def get_contacts(self):
        users = self.slack_object.api_call(
            "users.list"
            )
        
        members = users["members"]

        names = []
        counter = 0
        while counter < len(members):
            
            member = members[counter]
            names.append(member["name"])
            counter = counter + 1

        return names

    def get_message(self, target):
        users = self.slack_object.api_call(
            "users.list"
            )
        members = users["members"]
        counter = 0
        while counter < len(members):
            
            member = members[counter]
            if member["name"] == target:
                
                target_id = member["id"]
                
            counter = counter + 1

        channels = self.slack_object.api_call(
            "im.list"
            )
        channels = channels["ims"]
        counter = 0
        while counter < len(channels):
            
            if channels[counter]["user"] == target_id:
                target_channel_id = channels[counter]["id"]
                
            counter = counter + 1

        messages = self.slack_object.api_call(
            "im.history",
            channel=target_channel_id
            )

        messages = messages["messages"]

        id_to_name = {}
        counter = 0
        while counter < len(members):
            
            member = members[counter]
            id_to_name[member["id"]] = member["name"]
            counter = counter + 1

        results = []
        counter = 0
        while counter < len(messages):

            single_message = messages[counter]

            if single_message["type"] == "message":

                content = single_message["text"]
                
                try:
                    sender = id_to_name[single_message["user"]]
                except:
                    sender = single_message["username"]
                    
                if sender == target:
                    recipient = self.username
                else:
                    recipient = target
                if recipient == None:
                    recipient = "me"
                    
                time = single_message["ts"]
                time = datetime.fromtimestamp(float(time))
                
                results.append(GatherMessage(str(content),str(sender),str(recipient),time))
                
                counter = counter + 1

        return results

def get_token():
    #This one's yours Kevin
    token = raw_input("token: ")
    
    return token

def login(token,username,password):
    module_object = SlackService(token,username,password)
    
    return module_object

def test():
    username = "Boi"
    password = None
    token = get_token()
    module_object = login(token,username,password)

    recipient = "elk"
    message = "You're not my real dad!"
    target = "elk"
    
    result = module_object.get_message(target)
    print(result)
    module_object.send_message(recipient, message)
