import os
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def main():
    return 'Hello, World!'


@app.route('/privacy')
def privacy():
    return 'Privacy Policy will be posted here.'


@app.route('/webhook')
def webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge', '')
    
    if mode and token:
        if mode == 'subscribe' and token == os.environ.get('VERIFY_TOKEN', 'DEFAULT_VERIFY_TOKEN'):
            print('WEBHOOK_VERIFIED')
            
            return challenge, 200
        
        else:
            return '403 Forbidden', 403
    
    return 'Miss hub.mode or hub.verify_token', 403


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)