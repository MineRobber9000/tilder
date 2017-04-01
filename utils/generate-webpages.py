import cPickle,os
usersL=os.listdir("/home")
tilder_users=list()
for user in usersL:
	try:
		if os.path.exists(os.path.join("/home",user,".tilderrc")):
			output="# TildeTweets by "+cPickle.load(open(os.path.join("/home",user,".tilderrc"),"rb"))["name"]+" ("+user+")\n"
			if not os.path.exists(os.path.join("/home",user,".tildertimeline")):
				output += "None so far."
			else:
				for tweet in cPickle.load(open(os.path.join("/home",user,".tildertimeline"),"rb")):
					output += tweet + "\n----\n"
				output = output[:len(output)-6]
			fh = open(os.path.join(os.path.expanduser("~"),"public_html","tilder",user+".text"),"wb")
			fh.write(output)
			fh.close()
			tilder_users.append(user)
	except IOError as e:
		continue

users="# Users of tilder\n"
for tilder in tilder_users:
	users += "[{0!s}]({0!s}.html)  \n".format(tilder)

fh = open(os.path.join(os.path.expanduser("~"),"public_html","tilder","list.text"),"wb")
fh.write(users)

print("Finished!")
