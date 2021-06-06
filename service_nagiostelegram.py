#!/usr/bin/env python

# file     : service_nagiostelegram.py
# purpose  : send nagios notifications via Telegram bot
#
# author   : harald van der laan
# date     : 2021/06/03
# version  : v1.0.2
#
# fix      : sistemmsn 
#
# changelog:
# - v1.0.2      added pnp4nagios 
# - v1.0.1      added nagios command
# - v1.0.0      initial commit    


''' nagiosTelegram.py - small python script for sending nagios messages via a telegram
    bot. Please see BotFather for more info about telegram bots 
    
    https://core.telegram.org/bots
    
    Open telegram -> search for contacts: @BotFather
    send the following message to BotFather
    /newbot -> and answer the questions of BotFather
    
    # getting your telegram or group id
    1) send a message to you bot and surf to:
       https://api.telegram.org/bot<token>/getStatus
    2) download telegram-cli and send a message to the bot
    

    # service event
    ./service_nagiostelegram.py --token <token> --contact <contact|group_id> \ 
        --notificationtype 'service' --servicestate <OK|WARNING|CRITICAL|UNKNOWN> \ 
        --servicedesc <service description> --hostname <hostname> \ 
        --output <event message>

    
    define command {
        command_name    notify-service-by-telegram
        command_line    $USER1$/service_nagiostelegram.py --token <token> \
            --notificationtype service --contact "$CONTACTPAGER$" --notificationtype "$NOTIFICATIONTYPE$" \ 
            --servicestate "$SERVICESTATE$" --hostname "$HOSTNAME$" --servicedesc "$SERVICEDESC$" --output "$SERVICEOUTPUT$"
    }
    
    define contact {
        contact_name                    nagios telegram bot
        pager                           -<contact|group_id>
        service_notification_commands   notify-service-by-telegram
    }'''

from __future__ import print_function
import sys
import argparse
import json
import requests
import shutil
import time
import os
from pathlib import Path
from requests.auth import HTTPBasicAuth


#Historial de gráficos
graph_history  = 12
tstamp = time.time()
elapse = graph_history * 3600
start = graph_history - elapse
end = tstamp
# Url de tu pnp4nagios
pnp4nagios = "http://192.5.212.249/pnp4nagios/"

if os.path.exists("/usr/local/nagios/img/srvs.png"):
  os.remove("/usr/local/nagios/img/srvs.png")
  
def parse_args():
    ''' function for parsing arguments '''
    parser = argparse.ArgumentParser(description='Nagios notification via Telegram')
    parser.add_argument('-t', '--token', nargs='?', required=True)
    parser.add_argument('-o', '--object_type', nargs='?', required=True)
    parser.add_argument('--contact', nargs='?', required=True)
    parser.add_argument('--notificationtype', nargs='?')
    parser.add_argument('--hoststate', nargs='?')
    parser.add_argument('--hostname', nargs='?')
    parser.add_argument('--hostaddress', nargs='?')
    parser.add_argument('--servicestate', nargs='?')
    parser.add_argument('--servicedesc', nargs='?')
    parser.add_argument('--output', nargs='?')
    args = parser.parse_args()
    return args

def send_notification_photo(token, user_id, file_opened):
    ''' function for sending notification via Telegram bot '''
    url = 'https://api.telegram.org/bot' + token + '/sendPhoto'
    files = {'photo': file_opened}
    payload = {'chat_id': user_id}

    return requests.post(url, data=payload, files=files)    
    


def send_notification_message(token, user_id, message):
    ''' function for sending notification via Telegram bot '''
    url = 'https://api.telegram.org/bot' + token + '/sendMessage'
    payload = {'chat_id': user_id, 'text': message}

    return requests.post(url, data=payload)


def service_notification(args):
    ''' creating service notification message '''
    state = ''
    if args.servicestate == 'OK':
        state = u'\U00002705 '
    elif args.servicestate == 'WARNING':
        state = u'\U000026A0 '
    elif args.servicestate == 'CRITICAL':
        state = u'\U0001F525 '
    elif args.servicestate == 'UNKNOWN':
        state = u'\U00002753 '

    return '{}{}/{}: {}' .format(state.encode('utf-8'), args.hostname,
                                 args.servicedesc, args.output)

def main():
    ''' main function '''
    args = parse_args()
    user_id = int(args.contact)
    if args.object_type == 'service':
        message = service_notification(args)
    
    response = send_notification_message(args.token, user_id, message)
    
    my_file = Path("/usr/local/nagios/img/srvs.png")
    if my_file.is_file():
       response = send_notification_photo(args.token, user_id,  open('/usr/local/nagios/img/srvs.png', 'rb'))    

host = parse_args()

#Url for de  pnp4nagios services
srvurl =   str(pnp4nagios)+'image?host='+str(host.hostname)+'&srv='+str(host.servicedesc)+'&view=0&source=0&start'+str(round(start,0)).replace('0','')+'&end='+str(round(end,0)).replace('.0','')

#Download for img and user, passd
file = '/usr/local/nagios/img/srvs.png'
srvurl = requests.get(srvurl, auth=HTTPBasicAuth('nagiosadmin','systemahje'), stream=True)
if srvurl.status_code == 200:
    with open(file, 'wb') as f:
        srvurl.raw.decode_content = True
        shutil.copyfileobj(srvurl.raw, f)

if __name__ == "__main__":
    main()
    sys.exit(0)    