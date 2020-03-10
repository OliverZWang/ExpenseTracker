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
		Facebook.send_message(user.uid, "Welcome!!!", quick_replies = quick_replies)

		# Change Status from "New" to something else in DB
		# TO DO
		return False
	else:
		return True








def catch_all(user, msg):

	Facebook.send_message(user.uid, "Sorry, I don't understand. ")
