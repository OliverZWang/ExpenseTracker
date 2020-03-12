import Facebook
import datetime
import re


def check_new_user(user, webhookEvent):
    if user.user_status == "new":
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
        print("User Status Saved: {}".format(user.user_status))
        return False
    else:
        return True


def give_intro(user, webhookEvent):
    if webhookEvent['message']['text'].find('What is this') >= 0:
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
        return False
    else:
        return True


def get_length(user, webhookEvent):
    if webhookEvent['message']['text'].lower().find('get started') >= 0:
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
        return False
    else:
        return True


def catch_long_request(user, webhookEvent):
    if webhookEvent['message']['text'].lower().find("longer time") >= 0:
        Facebook.send_message(user.uid, "Nope")

        webhookEvent['message']['text'] = 'get started'

    return True


def ask_for_amount(user, webhookEvent):
    if webhookEvent['message']['text'].lower().find('week') >= 0 or webhookEvent['message']['text'].lower().find('day') >= 0:
        length = webhookEvent['message']['text'].split(' ')
        today = datetime.date.today()
        period = ''
        if length[1].find('week') >= 0:
            period = datetime.timedelta(weeks=int(length[0]))
        else:
            period = datetime.timedelta(days=int(length[0]))
        to_date = today + period
        # print(to_date)
        user.add_budgets(today, to_date, -1)

        Facebook.send_message(user.uid,
                              "How much would you like to spend for {} {}? (Please start with a dolar sign)".format(length[0], length[1]))
        return False
    else:
        return True


def set_amount(user, webhookEvent):
    if user.user_status == "not_in_budget_cycle" and webhookEvent['message']['text'].find('$') >= 0:
        total = float(webhookEvent['message']['text'][1:])
        # print(total)

        budget = user.get_budgets()[-1]
        budget.total = total
        budget.left = total
        budget.save()

        user.user_status = "in_budget_cycle"
        user.save()

        Facebook.send_message(user.uid, "Saved")

        return False


def catch_all(user, webhookEvent):
    Facebook.send_message(user.uid, "Sorry, I don't understand \"{}\". ".format(webhookEvent['message']['text']))

    if user.status == "in_budget_cycle":
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

    return False
