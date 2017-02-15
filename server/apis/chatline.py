import skype
import threading

# username = raw_input('username: ')
# password = raw_input('password: ')
username = 'gatherbois@gmail.com'
password = 'Andrew_PAD_#_1'
skype_object = skype.login(username, password)

def print_messages(api_obj):
    contacts = api_obj.get_contacts()
    contacts.remove('echo123')
    messages = []
    for c in contacts:
        messages += api_obj.get_messages(c.strip())
    for m in messages[::-1]:
        print '%s: %s' % (m.sender, m.body)

# while True:
#     print 'Who do you want to message?'
#     print skype_object.get_contacts()
#     recipient = raw_input('recipient: ')
#     message = raw_input('> ')
#     skype_object.send_message(recipient, message)
#     messages = skype_object.get_messages(recipient)

current_recipient = ''

while True:
    i = raw_input('%s> ' % current_recipient).strip() + ' '
    if i[0] == '/':
        command = i[1:i.index(' ')]
        if command == 'r':
            current_recipient = i[i.index(' ') + 1:].strip()
            print current_recipient
    else:
        skype_object.send_message(current_recipient, i)
        print_messages(skype_object)
        messages = skype_object.get_messages(current_recipient)
        for m in messages[::-1]:
            print '%s: %s' % (m.sender, m.body)