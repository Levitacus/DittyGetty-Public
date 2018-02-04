from gmusicapi import Mobileclient

api = Mobileclient()
logged_in = api.login('user@gmail.com', 'my-password', Mobileclient.FROM_MAC_ADDRESS)

if logged_in:
	print("success\n")
else:
	print("not successful\n")

programPause = raw_input("Press the <ENTER> key to continue...")