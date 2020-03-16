import Facebook
import datetime
from utils import *


def check_new_user(user, webhookEvent):
    debug('check_new_user', 'start')

    if user.user_status == "new":
        quick_replies = [
            {
                "content_type": "text",
                "title": "Tell Me More!",
                "payload": "tell_me_more",
                "image_url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/230/thinking-face_1f914.png"
            },
            {
                "content_type": "text",
                "title": "Get Started!",
                "payload": "get_started",
                "image_url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/230/thumbs-up-sign_1f44d.png"
            }
        ]

        Facebook.send_message(user.uid, "Welcome to Expense Tracker!\n"
                              + "We help you spend smarter every day by setting up budgets and tracking your spendings.",
                              quick_replies=quick_replies)

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

    if webhookEvent['message']['text'].lower().find('tell me more') >= 0 or webhookEvent['message']['text'].lower().find('what is this') >= 0:
        # print("Enter give_intro")
        quick_replies = [
            {
                "content_type": "text",
                "title": "Get Started! ",
                "payload": "get_started",
                "image_url": "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/facebook/230/thumbs-up-sign_1f44d.png"
            }
        ]

        Facebook.send_message(user.uid, "Welcome to Expense Tracker!\nWe help you spend smarter every day!\n"
                              + "To do so, we ask you to set up a budget for specific days and amounts. "
                              + "After that, we ask you to report every spending, and we will let you know what your spending power is.",
                              quick_replies=quick_replies)

        debug('give_intro', 'end false')
        return False
    else:
        debug('give_intro', 'end true')
        return True


def get_length(user, webhookEvent):
    debug('get_length', 'start')
    # TO DO: reply differently if user is in_budget_cycle
    if user.user_status == "not_in_budget_cycle":
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
                              "You haven't started a new budget period yet. "
                              + "Let's get to it. How long is your next budget period?",
                              quick_replies=quick_replies)

        user.user_status = "asked_for_length"
        user.save()
        # else:
        #     Facebook.send_message(user.uid,
        #                       "Welcome back! Please begin your report with a dollar sign.")
        debug('get_length', 'end false')
        return False
    else:
        debug('get_length', 'end true')
        return True


def catch_long_request(user, webhookEvent):
    debug('catch_long_request', 'start')
    # TO DO prompt the user to use a shorter time if input is too long
    if webhookEvent['message']['text'].lower().find("longer time") >= 0:
        # print("Enter catch_long_request")
        Facebook.send_message(user.uid, "A budget period longer than two weeks is difficult to track. "
                                        + "We encourage you to choose a shorter period.")

        webhookEvent['message']['text'] = 'get started'

    debug('catch_long_request', 'end true')
    return True


def ask_for_amount(user, webhookEvent):
    debug('ask_for_amount', 'start')
    # When a budge cycle is finished, 
    if user.user_status == "asked_for_length":
        # print("Enter ask_for_amount")
        if webhookEvent['message']['text'].lower().find('week') >= 0 or webhookEvent['message']['text'].lower().find(
                'day') >= 0:
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
                                  "How much would you like to spend for {} {}? (Please start with a dolar sign)".format(
                                      length[0], length[1]))
            user.user_status = "asked_for_amount"
            user.save()
        else:
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
                                  "You haven't started a budget period yet. Let's get to it. How long is your next budget period?",
                                  quick_replies=quick_replies)
        debug('ask_for_amount', 'end false')
        return False
    else:
        debug('ask_for_amount', 'end true')
        return True


def set_amount(user, webhookEvent):
    debug('set_amount', 'start')

    if user.user_status == "asked_for_amount":
        if webhookEvent['message']['text'].find('$') >= 0:
            # print("Enter set_amount")
            index = webhookEvent['message']['text'].find('$')
            total = float(webhookEvent['message']['text'][index + 1:])
            # print(total)

            budget = user.get_budgets()[-1]
            budget.total = total
            budget.left = total
            budget.save()
            Facebook.send_message(user.uid,
                                  "Saved. To report an expense, enter an amount starts with a dollar sign. ")
            user.user_status = "in_budget_cycle"
            user.save()
        else:
            Facebook.send_message(user.uid,
                                  "You haven't finished setting up your budget period yet. How much would you like to spend? (Please start with a dolar sign)")

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
                                      current_budget.left, days_left, round(current_budget.left / days_left, 2)
                                  ))

        else:
            Facebook.send_message(user.uid,
                                  'You have spent all the money for this period, there are {} day(s) left. '.format(
                                      days_left
                                  )
                                  + 'Better be more careful next time.')

            # Change name of status here
            user.user_status = 'not_in_budget_cycle'
            user.save()

        debug('initiate_report', 'end false')
        return False
    else:

        debug('initiate_report', 'end true')
        return True


def plain_message(user, webhookEvent):
    debug('plain_message', 'start')

    if webhookEvent['message']['text'].lower().find('report') >= 0:
        Facebook.send_message(user.uid, "To report an expense, enter an amount starts with a dollar sign. ")

        debug('plain_message', 'end false')
        return False

    elif webhookEvent['message']['text'].lower().find('spent nothing') >= 0:
        Facebook.send_message(user.uid, "Nice job, {}!".format(user.first_name))

        debug('plain_message', 'end false')
        return False

    else:

        debug('plain_message', 'end true')
        return True


def catch_all(user, webhookEvent):
    debug('catch_all', 'start')

    Facebook.send_message(user.uid, "Sorry, I don't understand \"{}\". ".format(webhookEvent['message']['text']))

    if user.user_status == "in_budget_cycle":
        quick_replies = [
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
