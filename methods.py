import Facebook
import datetime
import re


def check_new_user(user, webhookEvent):
    quick_replies = [
        {
            "content_type":"text",
            "title":"What is this?",
            "payload":"<POSTBACK_PAYLOAD>",
            # "image_url":""
        }
    ]

    if user.user_status == "new":
        Facebook.send_message(user.uid, "Welcome!", quick_replies=quick_replies)

        # Change Status from "New" to something else in DB
        user.user_status = "returning"
        user.save()
        print("User Status Saved: {}".format(user.user_status))
        return False
    else:
        return True


def give_intro(user, webhookEvent):
    quick_replies = [
        {
            "content_type":"text",
            "title":"Let's Get Started! ",
            "payload":"<POSTBACK_PAYLOAD>",
            # "image_url":""
        }
    ]

    if webhookEvent['message']['text'].find('What is this') >= 0:
        Facebook.send_message(user.uid, "Here goes a Short Intro",
                              quick_replies=quick_replies)
        return False
    else:
        return True


def get_length(user, webhookEvent):
    quick_replies = [
        {
            "content_type":"text",
            "title":"3 days",
            "payload":"valid_len",
            # "image_url":""
        },
        {
            "content_type":"text",
            "title":"5 days",
            "payload":"valid_len",
            # "image_url":""
        },
        {
            "content_type":"text",
            "title":"1 week",
            "payload":"valid_len",
            # "image_url":""
        },
        {
            "content_type":"text",
            "title":"2 weeks",
            "payload":"valid_len",
            # "image_url":""
        },
        {
            "content_type":"text",
            "title":"A Longer Time? ",
            "payload":"valid_len",
            # "image_url":""
        }
    ]

    if webhookEvent['message']['text'].lower().find('get started') >= 0:
        Facebook.send_message(user.uid,
                              "How long is your next budget period?",
                              quick_replies=quick_replies)
        return False
    else:
        return True


def catch_long_request(user, webhookEvent):
    quick_replies = [
        {
            "content_type":"text",
            "title":"3 days",
            "payload":"valid_len",
            # "image_url":""
        },
        {
            "content_type":"text",
            "title":"5 days",
            "payload":"valid_len",
            # "image_url":""
        },
        {
            "content_type":"text",
            "title":"1 week",
            "payload":"valid_len",
            # "image_url":""
        },
        {
            "content_type":"text",
            "title":"2 weeks",
            "payload":"valid_len",
            # "image_url":""
        },
        {
            "content_type":"text",
            "title":"A Longer Time? ",
            "payload":"valid_len",
            # "image_url":""
        }
    ]

    if webhookEvent['message']['text'].lower().find("longer time") >= 0:
        Facebook.send_message(user.uid,
                              "Nope",
                              quick_replies=quick_replies)
        return False
    else:
        return True


def ask_for_amount(user, webhookEvent):
    if webhookEvent['message']['text'].lower().find('week') >= 0 or webhookEvent['message']['text'].lower().find('day') >= 0:
        length = webhookEvent['message']['text'].split(' ')
        today = datetime.date.today()
        period = ''
        if length[1].find('week') >= 0:
            period = datetime.timedelta(weeks = int(length[0]))
        else:
            period = datetime.timedelta(days = int(length[0]))
        to_date = today + period
        # print(to_date)
        user.add_budgets(today, to_date, -1)
        Facebook.send_message(user.uid,
                              "How much would you like to spend for {} {}? (Please start with a dolar sign)".format(length[0], length[1]),
                              )
        return False
    else:
        return True


def set_amount(user, webhookEvent):
    if webhookEvent['message']['text'].find('$') >= 0:
        total = float(webhookEvent['message']['text'][1:])
        # print(total)
        user.add_total(total)
        Facebook.send_message(user.uid,
                              "Saved")


def catch_all(user, webhookEvent):
    Facebook.send_message(user.uid, "Sorry, I don't understand. ")
