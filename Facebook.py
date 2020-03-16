import os
import requests

from utils import *


FACEBOOK_GRAPH_API_URL = 'https://graph.facebook.com/v6.0'
FACEBOOK_ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', 'DEFAULT_VERIFY_TOKEN')


def get_user(uid):
    r = requests.get('{}/{}?access_token={}'.format(FACEBOOK_GRAPH_API_URL, str(uid), FACEBOOK_ACCESS_TOKEN))
    
    results = r.json()
    
    if 'error' in results:
        print(results['error'])
        
        return False, results['error'], ''
    else:
        return True, results['first_name'], results['last_name']


def send_message(uid, msg, quick_replies=None, message_type=None):
    json_data = {
            'recipient': {
                'id': uid
            },
            'message': {
                'text': msg
            }}
    if quick_replies is not None:
        json_data['message']['quick_replies'] = quick_replies
        # print(json_data)
    if message_type is not None:
        json_data['message_type'] = message_type

    r = requests.post(
        'https://graph.facebook.com/v6.0/me/messages?access_token=' + os.environ.get('ACCESS_TOKEN', 'DEFAULT_VERIFY_TOKEN'), 
        json=json_data,
        headers={'Content-type': 'application/json'})

    debug('send_message', 'message sent: ' + msg)


def sender_action(uid, action='typing_on'):
    json_data = {
        'recipient': {
            'id': uid
        },
        'sender_action': action
    }

    r = requests.post(
        'https://graph.facebook.com/v2.6/me/messages?access_token=' + os.environ.get('ACCESS_TOKEN', 'DEFAULT_VERIFY_TOKEN'),
        json=json_data,
        headers={'Content-type': 'application/json'}
    )


if __name__ == '__main__':
    status, first_name, last_name = get_user('3545504232158581')
    
    print(status, first_name, last_name)
    