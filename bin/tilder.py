import os,pwd,tempfile,cPickle,subprocess;
from email.mime.text import MIMEText;

version="Tilder v0.3"
descstring="the rough around the edges but still getting better version"

def setup():
	print("I don't know you, stranger. Let's get to know you, " + pwd.getpwuid(os.getuid()).pw_name + ".")
	print("Favorite text editor: ")
	print("1) nano")
	print("2) vi")
	print("3) ed")
	texteditor=raw_input("choose one: ")
	print("Personal Name - what should I call you?")
	name=raw_input("Name: ")
	print("Alright! You're ready to get started with Tilder!")
	settings = {"name":name}
	if texteditor == "1":
		settings.update({"editor":"nano"})
	elif texteditor == "2":
		settings.update({"editor":"vi"})
	elif texteditor == "3":
		settings.update({"editor":"ed"})
	else:
		settings.update({"editor":"nano"})
	cPickle.dump(settings,open(os.path.join(os.path.expanduser("~"),".tilderrc"),"wb"))

print("{0} - {1}".format(version, descstring))
print("")
if not os.path.exists(os.path.join(os.path.expanduser("~"),".tilderrc")):
	setup()
settings=cPickle.load(open(os.path.join(os.path.expanduser("~"),".tilderrc"),"rb"))
while True:
	print("What do you wish to do, "+settings["name"]+"?")
	print("1) Read a friend's timeline")
	print("2) Post to your own timeline")
	print("3) View your own timeline")
	print("4) Message a user")
	print("5) Quit")
	choice=raw_input("Choose an action: ")
	choice_int = int(choice)
	if choice_int == 1:
		print("Which friend?")
		name=raw_input("Username: ")
		if os.path.exists(os.path.join(os.path.expanduser("~"+name),".tildertimeline")):
			print("TildeTweets by "+cPickle.load(open(os.path.join(os.path.expanduser("~"+name),".tilderrc"),'rb'))["name"]+" ("+name+")\n----")
			for tweet in cPickle.load(open(os.path.join(os.path.expanduser("~"+name),".tildertimeline"),"rb")):
				print(tweet)
				print("----")
		else:
			print("Sorry, user not found.")
	elif choice_int == 2:
		if os.path.exists(os.path.join(os.path.expanduser("~"),".tildertimeline")):
			tweets=cPickle.load(open(os.path.join(os.path.expanduser("~"),".tildertimeline"),"rb"))
		else:
			tweets=list()
		temp = tempfile.NamedTemporaryFile(delete=False)
		subprocess.call([settings["editor"],temp.name])
		content=open(temp.name,"rb").read()
		tweets.reverse()
		tweets.append(content+"\nOn: "+subprocess.check_output(["date","+%Y-%m-%d"]))
		tweets.reverse()
		cPickle.dump(tweets, open(os.path.join(os.path.expanduser("~"),".tildertimeline"),"wb"))
		if "~" in content:
			userCounting=False
			userChars=list()
			for char in content:
				if userCounting:
					if char == " ":
						break
					userChars.append(char)
				else:
					if char == "~":
						userCounting=False
			if userChars in os.listdir("/home"):
				msg=MIMEText("~"+pwd.getpwuid(os.getuid()).pw_name+" mentioned you!\n\nTildeTweet Contents:\n"+content)
				msg['To']=userChars+"@tilde.town"
				msg['From']="tilder-mentions@tilde.town"
				msg['Subject']="You've been mentioned!"
				mail=os.popen("/usr/sbin/sendmail -t -oi","w")
				mail.write(msg.as_string())
				mail.close()
	elif choice_int == 3:
		print("TildeTweets by "+settings["name"]+" ("+pwd.getpwuid(os.getuid()).pw_name+")\n----")
		if not os.path.exists(os.path.join(os.path.expanduser("~"),".tildertimeline")):
			print("None so far...\n----")
			continue
		for tweet in cPickle.load(open(os.path.join(os.path.expanduser("~"),".tildertimeline"),"rb")):
			print(tweet)
			print("----")
	elif choice_int == 4:
		name=raw_input("User: ")
		if not name in os.listdir("/home"):
			print("Invalid user!")
			continue
		message=raw_input("Message: ")
		messtext=MIMEText(message)
		messtext['To']=name+"@tilde.town"
		messtext['From']=pwd.getpwuid(os.getuid()).pw_name+"@tilde.town"
		messtext['Subject']="Tilder message"
		p = os.popen("/usr/sbin/sendmail -t -oi",'w')
		p.write(messtext.as_string())
		p.close()
		print("Message sent!")
	elif choice_int == 5:
		break

print("\nbye!\n")
