
class GatherService(object):
    '''A standard inteface to inherit from in each API'''
    def get_contacts(self):
        '''Returns all contacts from service'''
        raise NotImplementedError("Must implement get_contacts")
    def get_messages(self, contact_name):
        '''Returns GatherMessages given a contact'''
        raise NotImplementedError("Must implement get_messages")
    def send_message(self, contact_name, message):
        '''Sends (string) message to contact name'''
        raise NotImplementedError("Must implement send_message")
