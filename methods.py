import Facebook
import datetime
from utils import *


def check_new_user(user, webhookEvent):
    debug('check_new_user', 'start')

    if user.user_status == "new":
        # print("Enter check_new_user")
        quick_replies = [
            {
                "content_type": "text",
                "title": "What is this?",
                "payload": "<POSTBACK_PAYLOAD>",
                "image_url":"https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/230/thinking-face_1f914.png"
            }
        ]

        Facebook.send_message(user.uid, "Welcome!", quick_replies=quick_replies)

        # Change Status from "New" to something else in DB
        user.user_status = "not_in_budget_cycle"
        user.save()
        debug('check_new_user', "User Status Saved: {}".format(user.user_status))

        debug('check_new_user', 'end false')
        return False
    else:

        debug('check_new_user', 'end true')
        return True


def give_intro(user, webhookEvent):
    debug('give_intro', 'start')

    if webhookEvent['message']['text'].find('What is this') >= 0:
        # print("Enter give_intro")
        quick_replies = [
            {
                "content_type": "text",
                "title": "Let's Get Started! ",
                "payload": "<POSTBACK_PAYLOAD>",
                # "image_url":""
            }
        ]

        Facebook.send_message(user.uid, "Here goes a Short Intro",
                              quick_replies=quick_replies)

        debug('give_intro', 'end false')
        return False
    else:
        debug('give_intro', 'end true')
        return True


def get_length(user, webhookEvent):
    debug('get_length', 'start')

    if webhookEvent['message']['text'].lower().find('get started') >= 0:
        # print("Enter get_length")
        quick_replies = [
            {
                "content_type": "text",
                "title": "3 days",
                "payload": "valid_len",
                # "image_url":""
            },
            {
                "content_type": "text",
                "title": "5 days",
                "payload": "valid_len",
                # "image_url":""
            },
            {
                "content_type": "text",
                "title": "1 week",
                "payload": "valid_len",
                # "image_url":""
            },
            {
                "content_type": "text",
                "title": "2 weeks",
                "payload": "valid_len",
                # "image_url":""
            },
            {
                "content_type": "text",
                "title": "A Longer Time? ",
                "payload": "valid_len",
                # "image_url":""
            }
        ]

        Facebook.send_message(user.uid,
                              "How long is your next budget period?",
                              quick_replies=quick_replies)

        debug('get_length', 'end false')
        return False
    else:
        debug('get_length', 'end true')
        return True


def catch_long_request(user, webhookEvent):
    debug('catch_long_request', 'start')

    if webhookEvent['message']['text'].lower().find("longer time") >= 0:
        # print("Enter catch_long_request")
        Facebook.send_message(user.uid, "Nope")

        webhookEvent['message']['text'] = 'get started'

    debug('catch_long_request', 'end true')
    return True


def ask_for_amount(user, webhookEvent):
    debug('ask_for_amount', 'start')

    if user.user_status != "in_budget_cycle" and webhookEvent['message']['text'].lower().find('week') >= 0 or webhookEvent['message']['text'].lower().find('day') >= 0:
        # print("Enter ask_for_amount")

        length = webhookEvent['message']['text'].split(' ')
        today = datetime.date.today()
        period = ''
        if length[1].find('week') >= 0:
            period = datetime.timedelta(weeks=int(length[0]))
        else:
            period = datetime.timedelta(days=int(length[0]))
        to_date = today + period
        # print(to_date)
        user.add_budget(today, to_date, -1)

        Facebook.send_message(user.uid,
                              "How much would you like to spend for {} {}? (Please start with a dolar sign)".format(length[0], length[1]))

        debug('ask_for_amount', 'end false')
        return False
    else:
        debug('ask_for_amount', 'end true')
        return True


def set_amount(user, webhookEvent):
    debug('set_amount', 'start')

    if user.user_status != "in_budget_cycle" and webhookEvent['message']['text'].find('$') >= 0:
        # print("Enter set_amount")
        total = float(webhookEvent['message']['text'][1:])
        # print(total)

        budget = user.get_budgets()[-1]
        budget.total = total
        budget.left = total
        budget.save()

        user.user_status = "in_budget_cycle"
        user.save()

        Facebook.send_message(user.uid, "Saved")

        debug('set_amount', 'end false')
        return False
    else:
        return True


def initiate_report(user, webhookEvent):
    debug('initiate_report', 'start')

    # For now, the user has to enter exactly "$<amount>"
    if user.user_status == "in_budget_cycle" and webhookEvent['message']['text'].find('$') >= 0:
        amount = float(webhookEvent['message']['text'][1:])

        current_budget = user.get_budgets()[-1]

        current_budget.addTransaction(amount, '')

        days_left = (current_budget.to_date - datetime.datetime.date(datetime.datetime.now())).days

        if current_budget.left > 0:
            Facebook.send_message(user.uid,
                                  'Thanks for letting me know. You have ${} left for {} day(s). That\'s ${} per day.'.format(
                                      current_budget.left, days_left, current_budget.left / days_left
                                  ))

        else:
            Facebook.send_message(user.uid,
                                  'You have spent all the money for this period, there are {} day(s) left. '.format(
                                      days_left
                                  )
                                  + 'Better be more careful next time.')

            user.user_status = 'not_in_budget_cycle'
            user.save()

        debug('initiate_report', 'end false')
        return False
    else:

        debug('initiate_report', 'end true')
        return True


def catch_all(user, webhookEvent):
    debug('catch_all', 'start')

    Facebook.send_message(user.uid, "Sorry, I don't understand \"{}\". ".format(webhookEvent['message']['text']))

    if user.user_status == "in_budget_cycle":
        quick_replies = [
            {
                "content_type": "text",
                "title": "What should I do next?",
                "payload": "whats_next",
                "image_url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/230/thinking-face_1f914.png"
            },
            {
                "content_type": "text",
                "title": "Report a spending",
                "payload": "report",
                "image_url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/230/money-with-wings_1f4b8.png"
            }
        ]
    else:
        quick_replies = [
            {
                "content_type": "text",
                "title": "What is this?",
                "payload": "whats_this",
                "image_url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/230/thinking-face_1f914.png"
            }
        ]

    Facebook.send_message(user.uid, "Please choose from one of the options below.", quick_replies=quick_replies)

    debug('catch_all', 'end false')
    return False
