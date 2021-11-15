# Simple Reddit Bot
# One of many ways to access and respond to information flows on Reddit.
# https://praw.readthedocs.io/en/latest/tutorials/reply_bot.html
# Produce a (canned) response to a collection of possible questions found in Reddit feeds
# requires: praw; install with pip install praw (https://praw.readthedocs.io/en/stable/)
# requires an active Reddit account
# set up an app (https://healeycodes.com/reddit-bot-tutorial)
# and get the credentials as described
# use LMGTFY (Let Me Google That For You) to suggest a search (https://lmgtfy.app/)
# Oct 2021
#
# Your task is to create an interesting variation of this simple bot.
#---------------------------------------------------------------------------------------
import os, sys, time
import praw
import getpass
from urllib.parse import quote_plus

mpass = 'your Reddit password'
mid = 'your ID'
msecret = 'your secret'
mname = 'your Reddit name'
magent = 'sometest_v1 (by /u/your Reddit name)'

reddit = praw.Reddit(
	client_id = mid,
	client_secret = msecret,
	password = mpass,
	user_agent = magent,
	username = mname)

#test access
#print(reddit.user.me())

QUESTIONS = ["what is", "who is", "who was", "what are"]
REPLY_TEMPLATE = "[Hmm. that is a tricky one. Depends who asks. Lets see what the web says...](https://lmgtfy.com/?q={})"

subreddit = reddit.subreddit("AskReddit")

print('\nHere are 3 short questions (less that 10 letters long) currently on AskReddit...')
tlim = 10
clim = 3
collection = []

for submission in subreddit.stream.submissions():
	if(len(submission.title.split()) < tlim):
		collection.append(submission)
		if(len(collection) > clim):
			break

#check the results
for sub in collection:
	print (sub.title)

print('\nLooking for Reddit questions similar to those in the QUESTIONS list and generating responses...')

for sub in collection:
	for question in QUESTIONS:
		if question in sub.title.lower():
			print('Here is the template question: ', question)
			print('Here is the reddit question: ', sub.title.lower())
			url_title = quote_plus(sub.title)
			reply_text = REPLY_TEMPLATE.format(url_title)
			print("Replying to: ", sub.title)
			print("Replying with: ", reply_text)
			sub.reply(reply_text)
			#break out of the loop after one response.
			break
print('\DONE')
