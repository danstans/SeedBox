from __future__ import print_function
import os
import base64
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from subprocess import call
import time



try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET = 'client_secret.json'
MESSAGE_SENDERS = ['stansberry2295@gmail.com', 'dstansbe@ucsc.edu']
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPES)
	creds = tools.run_flow(flow, store, flags) if flags else tools.run(flow,store)

SERVICE = build('gmail', 'v1', http=creds.authorize(Http()))

def getMessage():
	messages = SERVICE.users().messages().list(userId='me', q='label:unread').execute().get('messages', [])
	for message in messages:
		oneMessage = SERVICE.users().messages().get(userId='me', id=message['id'], format='full').execute()
		oneMessageSub = oneMessage['payload']['headers']
		msgBody = ""
		bodyPart = oneMessage['payload']['parts']
					  #### THIS is the torrent Link
		msgSubject = ""                 #### This is the Folder to download it to, also check for passoword
		msgSender = ""
		i= 0
		while i < len(oneMessageSub):
			query = oneMessageSub[i]['name']
			if query == 'Subject':
				msgSubject = oneMessageSub[i]['value']
			if query== 'From':
				msgSender = oneMessageSub[i]['value']
			i+=1

		a=0
		while a < len(bodyPart):
			if (bodyPart[a]['mimeType'] == 'text/plain'):
				msgBody = base64.b64decode(bodyPart[a]['body']['data'])
			a+=1

		torrentDir = "/home/alec/"
		if (key in msgSender for key in MESSAGE_SENDERS):
		    modLabelIds = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
    		modMessage = SERVICE.users().messages().modify(userId='me', id=message['id'], body=modLabelIds).execute()
    		torrentDir += msgSubject
    		callTransmission(torrentDir, msgBody)
    		##Call tranmission torrent client using command line, with link (msgBody) and Directory (msgSubject)



def callTransmission(strDirectory, strTorrentLink):
	returnCode = call(['transmission-remote', '-w', strDirectory, '-a', strTorrentLink])
	return

while True:
    print("searching for messages")
    getMessage()
    print("sleeping for 20 seconds")
    time.sleep(20)








