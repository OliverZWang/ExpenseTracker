import os
from flask import Flask, request
import requests

from User import User
from methods import *

app = Flask(__name__)

method_list = [check_newuser, catch_all]

@app.route('/')
def main():
    return 'Hello, World!'


@app.route('/privacy')
def privacy():
    return 'Privacy Policy will be posted here.'


@app.route('/webhook', methods=['GET'])
def webhook_get():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge', '')
    
    if mode and token:
        if mode == 'subscribe' and token == os.environ.get('VERIFY_TOKEN', 'DEFAULT_VERIFY_TOKEN'):
            print('WEBHOOK_VERIFIED')
            
            return challenge
        
        else:
            return '403 Forbidden', 403
    
    return 'Miss hub.mode or hub.verify_token', 403


@app.route('/webhook', methods=['POST'])
def webhook_post():
    body = request.get_json()
    
    if body["object"] == "page":
        for entry in body["entry"]:
            for webhookEvent in entry['messaging']:
                
                uid = webhookEvent['sender']['id']
                
                user = User(uid)
                
                for method in method_list:
                    if (!method(user, "")):
                        break
                
                # send_message(sid, 'Test!')
            
        return 'EVENT_RECEIVED'
    
    return '404 Not Found', 404


def send_message(rid, msg):
    r = requests.post(
        'https://graph.facebook.com/v6.0/me/messages?access_token=' + os.environ.get('ACCESS_TOKEN', 'DEFAULT_VERIFY_TOKEN'), 
        json = {
            'recipient': {
                'id': rid
            },
            'message': {
                'text': msg
            }
        },
        headers = {'Content-type': 'application/json'})


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)