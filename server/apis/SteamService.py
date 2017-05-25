import steamapi
import vsteamapi
from datetime import datetime
from GatherService import GatherService
import GatherMessage

class SteamService(GatherService):
    
    def __init__(self, usrnm, psswrd):
        self.steam = steamapi.steamapi()
        vsteamapi.core.APIConnection(api_key="98F11B21A6560EA46E01FBF3E1D4F9B8", validate_key = True)
        status = self.steam.login(username= usrnm, password= psswrd)
        while status != steamapi.enums.LoginStatus.LoginSuccessful:
            if status == steamapi.enums.LoginStatus.TwoFactor:
                token = raw_input("Two-factor Token: ")
                status = self.steam.retry(twofactor=token)
            elif status == steamapi.enums.LoginStatus.SteamGuard:
                steamguard = raw_input("SteamGuard Code: ")
                status = self.steam.retry(steamguard=steamguard)
            elif status == steamapi.enums.LoginStatus.Captcha:
                captcha = raw_input("CAPTCHA: ")
                status = self.steam.retry(captcha=captcha)
        self.me = vsteamapi.user.SteamUser(userurl = usrnm)
        
    def get_contacts(self):
        steam_contacts = self.me.friends
        names = []
        for person in steam_contacts:
            names.append(str(person.name))
        return names
    
    def get_messages(self, contact_name):
        steam_msgs = self.steam.chat.get_chat_history(self.get_ID(contact_name))
        gather_msgs = []
        for m in steam_msgs:
            gather_msgs.append(self.convert_message(contact_name,m))
        return gather_msgs
    
    def send_message(self, contact_name, message):
        self.steam.chat.login()
        self.steam.chat.send_message(self.get_ID(contact_name), message)
        self.steam.chat.logout()
        return True

    def get_ID(self, contact_name):
        #gets steam id from contact name
        dict = {}
        for person in self.me.friends:
            dict[person.name] = person.id
        return dict[contact_name]

    def convert_message(self, contact_name, steam_msg):
        body = str(steam_msg.message)
        senderID = steam_msg.steam_id
        sender = self.get_Name(senderID)
        print(sender)
        recipient = self.get_Recipient_Name(contact_name, senderID)
        print(recipient)
        time = self.convertDate(steam_msg.timestamp)
        return GatherMessage.GatherMessage(body, sender, recipient, time)

    def convertDate(self, tstamp):
        return datetime.fromtimestamp(tstamp/1000)

    def get_Recipient_Name(self, contact, senderID):
        if(str(senderID) == str(self.me.id)):
            return contact
        return self.me.name

    def get_Name(self, senderID):
        if(str(senderID) == str(self.me.id)):
            return self.me.name
        dict = {}
        for person in self.me.friends:
            dict[person.id] = person.name
        return dict[senderID]
