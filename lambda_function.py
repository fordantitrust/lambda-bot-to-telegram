# ==== Environment variables ====
# CHAT_ID 
# TOKEN 

import os
import json
import logging
from urllib import request, parse, error

def lambda_handler(event, context):

    url = 'https://api.telegram.org/bot%s/sendMessage' % os.environ['TOKEN']
    
    print("json.dumps=event: " + json.dumps(event) + "\r\n")
    
    message_parsed = (json.loads(event['Records'][0]['Sns']['Message']))
    msg = "(empty)"
    
    print("json.dumps=message_parsed: " + json.dumps(message_parsed) + "\r\n")

    # ==== BEGIN RULE ====


    if('AlarmName' in message_parsed):
        msg = message_parsed['NewStateValue'] + ": " + message_parsed['AlarmName']

    
    # ==== END RULE ====

    print("msg: " + msg +"\r\n")
    
    data = parse.urlencode({'chat_id': os.environ['CHAT_ID'], 'text': msg})
    
    try:
        # Send the SNS message (notification) to Telegram
        request.urlopen(url, data.encode('utf-8'))
    except error.HTTPError as e:
        print('Failed to send the SNS message below')
        response = json.load(e)
        if 'description' in response:
            print(response['description'])
        raise e