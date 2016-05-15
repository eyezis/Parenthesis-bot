import os
import sys 
import time
import re

reddit_username = "parenthesis_bot"

# regex below matches typical characters that usually precede an emoticon (;:-'), also removes ('s that are in quotes
ba = re.escape(":-;'^=*x")
removeEmotes = re.compile("[" + ba + "\\\\]\(+|\(+[" + ba + "]|[\'\"]\([\'\"]")

#print "[" + ba + "\\\\]\(+|\(+[" + ba + "]|[\'\"]\([\'\"]"

repls = ('（', '('), ('）', ')')

reload(sys) 
sys.setdefaultencoding('utf-8') 

def log(msg):
	try:
		print msg
	except:
		pass
	with open("log.txt", "a") as f:
		f.write(time.strftime("%Y-%m-%d %X") + " " + msg + "\n")

def parenCountOpen(str):
	return str.count("(") - str.count(")")

def stringProc(s):
	s = s.replace(" ", "")
	s = reduce(lambda a, kv: a.replace(*kv), repls, s)
	return removeEmotes.sub("", s)