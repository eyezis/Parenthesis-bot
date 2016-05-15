# -*- coding: utf-8 -*-

exec(open('common.py').read())

def tryComment(c, msg):
	while True:
		try:
			log("Trying to reply to: {}".format(c.author.name))
			log(c.permalink)
			c.reply(msg)
			log("Success!")
			return
		except Exception as e:
			log("Error! " + str(e))
			if '403' in str(e):
				log("Got banned from " + c.subreddit)
				addBannedSub(c.subreddit)
			return

def is_summon_chain(post):
	if not post.is_root:
		parent_comment_id = post.parent_id
		parent_comment = r.get_info(thing_id=parent_comment_id)
		if parent_comment.author != None and str(parent_comment.author.name) == 'parenthesis_bot': #TODO put your bot username here
			return True
		else:
			return False
	else:
		return False

bannedSubs = ""
def loadBannedSubs():
	global bannedSubs
	f = open("banned.txt", 'r')
	try:
		bannedSubs = f.read()
	except:
		bannedSubs = ""
	f.close()   

def addBannedSub(s):
	global bannedSubs
	bannedSubs += " " + s
	f = open("banned.txt", 'w')
	f.write(bannedSubs)
	f.close()



if __name__ == '__main__':
	loadBannedSubs()

	import praw
	r = praw.Reddit('Parenthesis auto closer, by /u/eyezis | see https://xkcd.com/859 for more info')
	
	r.login(reddit_username, os.environ['redditpw'])

	for c in praw.helpers.comment_stream(r, 'all'):
		if str(c.subreddit).lower() in bannedSubs.lower():
			continue
		
		try:
			if "BOOK" in c.submission.title:
				continue
		except Exception as e:
			print "Error checking title " + c.permalink
			pass
		
		#sys.stdout.write(c.author.name + "|" + str(c.subreddit) + "|")
		#print c

		pCount = parenCountOpen(stringProc(c.body))
		if pCount > 0:
			c.refresh()
			if is_summon_chain(c):
				log("summon chain detected! " + c.permalink)
				continue
			if reddit_username not in [reply.author.name for reply in c.replies]:
				tryComment(c, ")"*pCount)
				log("")
