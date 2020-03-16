from flask import Flask, request

import Facebook
from User import User
from methods import *
from Db import db

app = Flask(__name__)

method_list = [check_new_user, give_intro, catch_long_request, get_length, ask_for_amount,
               set_amount, initiate_report, plain_message, catch_all]


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

                Facebook.sender_action(user.uid, 'mark_seen')
                Facebook.sender_action(user.uid, 'typing_on')
                
                for method in method_list:
                    if method(user, webhookEvent):
                        continue
                    # print("Got here")
                    break
            
        return 'EVENT_RECEIVED'
    
    return '404 Not Found', 404


@app.route('/cron')
def cron():
    # 0 reminder, 1 daily reporter
    cron_type = request.args.get('type')

    if cron_type is None:
        warning('cron', 'Type should not be none')

        return 'Type should not be none', 404

    user_collection = db.users

    users = user_collection.find({'user_status': 'in_budget_cycle'}, {'uid': 1})

    if cron_type == '0':
        debug('cron', 'start reminder')

        for tmp in users:
            user = User(tmp['uid'])

            budget = user.get_budgets()[-1]

            if len(budget.getTransaction(today=True)) == 0:
                quick_replies = [
                    {
                        "content_type": "text",
                        "title": "I spent nothing today.",
                        "payload": "spent_nothing"
                    },
                    {
                        "content_type": "text",
                        "title": "I will report now!",
                        "payload": "report_now"
                    }
                ]

                Facebook.send_message(user.uid,
                                      "Hey {}, I noticed that you have not reported any spending today. ".format(user.first_name)
                                      + "Did you actually spend nothing today?", quick_replies=quick_replies)

        debug('cron', 'end reminder')

        return 'Success'

    elif cron_type == '1':
        debug('cron', 'start reporter')

        for tmp in users:
            user = User(tmp['uid'])

            budget = user.get_budgets()[-1]

            transactions = budget.getTransaction(today=True)

            total = 0

            for tran in transactions:
                total += tran.amount

            days_left = (budget.to_date - datetime.datetime.date(datetime.datetime.now())).days - 1

            Facebook.send_message(user.uid,
                                  "You have spent ${} today. ".format(total)
                                  + "You have ${} left for this period, that's ${} per day.".format(round(budget.left, 2), round(budget.left / days_left, 2)))

        debug('cron', 'end reporter')

        return 'Success'

    else:
        warning('cron', 'Unknown cron type: ' + cron_type)

        return 'Unknown cron type: ' + cron_type, 404


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    