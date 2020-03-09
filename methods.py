import Facebook

def check_new_user(user, msg):

	if user.user_status == "new":
		Facebook.send_message(user.uid, "Welcome!")
		return False

	else:
		return True

def catch_all(user, msg):

	Facebook.send_message(user.uid, "Sorry, I don't understand. ")