import praw
import time
import re
import os

MESSAGE_REPLY = 'LEO is the Nike SNKRS app protocol that stands for "Let Everyone Order". Users on the SNKRS app have about 2-3 minutes to submit in their purchase information and to be put in line. After a few minutes of being in line, Nike will select users randomly to complete the purchases.'
MESSAGE_FOOTER = """


***


^I ^am ^a ^robot. ^Beep ^boop.
^(`Message me` to talk to my creator.)

"""

comments_replied_id = []


def main():
	comments_replied_id = get_saved_comments()
	reddit = authenticate()
	while True:
		run_bot(reddit, comments_replied_id)

def authenticate():
	print('Authenticating...')
	reddit = praw.Reddit('SNKRS_BOT', user_agent='SNKRS bot by /u/jae_young')

	print('Authenticated as {}'.format(reddit.user.me()))
	return reddit

def run_bot(reddit, idlist):
	print('Going through 30 comments...')
	for comments in reddit.subreddit('Sneakers').comments(limit=30):
		if "LEO" in comments.body and comments.id not in comments_replied_id and comments.author != reddit.user.me():
			print('Found comment with "LEO"... now replying')	
			
			reply = '# LEO' + "\n\n"
			reply += MESSAGE_REPLY + "\n"
			reply += MESSAGE_FOOTER

			comments.reply(reply)

			print('Comment', comments.id, 'replied.')

			comments_replied_id.append(comments.id)

			with open('comments.txt', 'a') as f:
				f.write(comments.id + "\n")

	print('Sleeping for 15 seconds...')
	time.sleep(15)

def get_saved_comments():
	if not os.path.isfile('comments.txt'):
		comments_replied_id = []
	else:
		with open('comments.txt', 'r') as f:
			comments_replied_id = f.read()
			comments_replied_id = comments_replied_id.split("\n")
			comments_replied_id = filter(None, comments_replied_id)

	return comments_replied_id


if __name__ == '__main__':
	main()
