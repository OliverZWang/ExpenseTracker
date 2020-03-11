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
		user.user_status = "returning"
		# Change Status from "New" to something else in DB
		user.save()
		print("User Status Saved: {}".format(user.user_status))
		return False
	else:
		return True

def give_intro(user, msg):
	print("Got here")
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






def catch_all(user, msg):

	Facebook.send_message(user.uid, "Sorry, I don't understand. ")
