from slackclient import SlackClient

def get_token():
    #This one's yours Kevin
    token = raw_input("token: ")
    
    return token

def initialize_object(token):
    
    slack_object = SlackClient(token)

    return slack_object

def send_message(slack_object,message,channel):

    try_channel = channel

    try:
        slack_object.api_call("chat.postMessage",channel=try_channel,text=message)
        return True

    except:
        return False

def get_channel_names(slack_object):

    channel_object = slack_object.api_call("channels.list")
    channel_dictionary = channel_object["channels"]

    counter = 0
    channel_names = []
    while counter < len(channel_dictionary):
        
        single_channel = channel_dictionary[counter]
        channel_names.append(single_channel["name"])
        counter = counter + 1

    return channel_names

def get_channel_id(slack_object,name):

    channel_object = slack_object.api_call("channels.list")
    channel_dictionary = channel_object["channels"]

    counter = 0
    while counter < len(channel_dictionary):
        
        single_channel = channel_dictionary[counter]
        
        if single_channel["name"] == name:

            print("returning id: " + single_channel["id"])
            
            return single_channel["id"]
        
        counter = counter + 1
    
    return False

def join_channel(slack_object,channel):

    try:
        slack_object.api_call("join.channel",channel)
        return True
    
    except:
        return False

def leave_channel(slack_object,channel):
    
    try:
        slack_object.api_call("leave.channel",channel)
        return True
    
    except:
        return False

def get_latest_message(slack_object,channel_id):

    channel_object = slack_object.api_call("channels.info",channel=channel_id)

    channel_dictionary = channel_object["channel"]

    messages = channel_dictionary["latest"]

    return messages
