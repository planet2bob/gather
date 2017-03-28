import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr

session = botocore.session.get_session()
ACCESS_KEY = session.get_credentials().access_key
SECRET_KEY = session.get_credentials().secret_key
SESSION_TOKEN = session.get_credentials().token

dynamodb = boto3.resource('dynamodb', 
                            aws_access_key_id=ACCESS_KEY, 
                            aws_secret_access_key=SECRET_KEY, 
                            aws_session_token=SESSION_TOKEN,
                            region_name='us-west-2')

TABLE = dynamodb.Table('gather')

def put_item(item):
    if 'username' not in item.keys():
        raise ValueError("put_item's item must have key 'username'")
    TABLE.put_item(
        Item=item
    )

def update_item(item_key, keys,):
    key_options = 'abcdefghijklmnopqrstuvwxyz'
    attr_values = {}
    update_expression = 'set '
    for i, key in enumerate(keys):
        update_expression += key + ' = :' + key_options[i] + ', '
        attr_values[':' + key_options[i]] = keys[key]
    update_expression = update_expression[:-2]
    TABLE.update_item(
        Key={'username': item_key},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=attr_values
    )

def get_item(item_key):
    result = TABLE.get_item(Key={'username':item_key})
    try:
        return result['Item']
    except KeyError:
        print 'Username "%s" does not exist in DB!' % item_key
        return None

def remove_item(item_key):
    result = TABLE.delete_item(Key={'username':item_key})
    status_code = result['ResponseMetadata']['HTTPStatusCode']
    return status_code

def create_account(username, password_hash):
    account_object = {
        'username': username,
        'password': password_hash,
        'services': []
    }
    put_item(account_object)

def add_service_to_account(username, service_obj):
    account = get_item(username)
    new_services = account['services'] + [service_obj]
    update_item(username, {
        'services': new_services
    })

# create_account('maxsun', '217398hdksayd89as')
add_service_to_account('maxsun', {
    'service': 'skype',
    'username': 'maxskype',
    'token': '172312ksdjah8721'
})
