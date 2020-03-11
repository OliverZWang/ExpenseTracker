import Facebook


def check_new_user(user, msg):
	quick_replies = [
	      {
	        "content_type":"text",
	        "title":"What is this?",
	        "payload":"<POSTBACK_PAYLOAD>",
	        # "image_url":""
	      }
	    ]
	if user.user_status == "new":
		Facebook.send_message(user.uid, "Welcome!", quick_replies = quick_replies)

		# Change Status from "New" to something else in DB
		user.user_status = "returning"
		user.save()
		print("User Status Saved: {}".format(user.user_status))
		return False
	else:
		return True

def give_intro(user, msg):

	quick_replies = [
	      {
	        "content_type":"text",
	        "title":"Let's Get Started! ",
	        "payload":"<POSTBACK_PAYLOAD>",
	        # "image_url":""
	      }
	    ]
	if msg.find('What is this') >= 0:
		Facebook.send_message(user.uid, "Here goes a Short Intro", 
			quick_replies = quick_replies)
		return False
	else: 
		return True

def get_length(user, msg):
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
	if msg.lower().find('get started') >= 0:
		Facebook.send_message(user.uid, 
			"How long is your next budget period?", 
			quick_replies = quick_replies)
		return False
	else:
		return True

def catch_long_request(user, msg):

	if msg.lower().find("can i choose a longer time") >= 0:
		Facebook.send_message(user.uid, 
			"Nope")
		return False
	else:
		return True

def ask_for_amount(user, msg):

	if msg.lower().find('week') >= 0 or msg.lower().find('day') >= 0:
		length = msg.split(' ')
		Facebook.send_message(user.uid, 
			"How much would you like to spend for {} {}?".format(length[0], length[1]))
		return False
	else:
		return True


def catch_all(user, msg):

	Facebook.send_message(user.uid, "Sorry, I don't understand. ")
