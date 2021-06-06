#!/usr/bin/env python

# file     : host_nagiostelegram.py
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
# - v1.0.0      initial commit                                          (harald)


''' host_nagiostelegram.py - small python script for sending nagios messages via a telegram
    bot. Please see BotFather for more info about telegram bots 
    
    https://core.telegram.org/bots
    
    Open telegram -> search for contacts: @BotFather
    send the following message to BotFather
    /newbot -> and answer the questions of BotFather
    
    # getting your telegram or group id
    1) send a message to you bot and surf to:
       https://api.telegram.org/bot<token>/getStatus
    2) download telegram-cli and send a message to the bot
    
    usage:
    # host event
    ./host_nagiostelegram.py --token <token> --contact <contact|group_id> \ 
        --notificationtype 'host' --hoststate <UP|DOWN|UNREACHABLE> \ 
        --hostname <hostname> --hostaddress <ipaddress> \ 
        --output <event message>
        
    # nagios configuration
    define command {
        command_name    notify-host-by-telegram
        command_line    $USER1$/host_nagiostelegram.py --token <token> \ 
            --notificationtype host --contact "$CONTACTPAGER$" --notificationtype "$NOTIFICATIONTYPE$" \ 
            --hoststate "$HOSTSTATE$" --hostname "$HOSTNAME$" --hostaddress "$HOSTADDRESS$" --output "$HOSTOUTPUT$"
    }
    
    
    define contact {
        contact_name                    nagios telegram bot
        pager                           -<contact|group_id>
        host_notification_commands      notify-host-by-telegram
    }'''

from __future__ import print_function
import sys
import argparse
import json
import requests
import shutil
import time
from requests.auth import HTTPBasicAuth


graph_history  = 12
tstamp = time.time()
elapse = graph_history * 3600
start = graph_history - elapse
end = tstamp
pnp4nagios = "http://192.5.212.249/pnp4nagios/"
hostsimg = open('/usr/local/nagios/img/hosts.png', 'rb')
srvhost = "_HOST_"

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


def host_notification(args):
    ''' creating host notification message '''
    state = ''
    if args.hoststate == 'UP':
        state = u'\U00002705 '
    elif args.hoststate == 'DOWN':
        state = u'\U0001F525 '
    elif args.hoststate == 'UNREACHABLE':
        state = u'\U00002753 '

    return '{}{} ({}): {}' .format(state.encode('utf-8'), args.hostname,
                                   args.hostaddress, args.output)

def main():
    ''' main function '''
    args = parse_args()
    user_id = int(args.contact)
    if args.object_type == 'host':
        message = host_notification(args)
    

    response = send_notification_message(args.token, user_id, message)
    respones = send_notification_photo(args.token, user_id, hostsimg)


host = parse_args()

''' Url for de  pnp4nagios services'''
hostsurl =   str(pnp4nagios)+'image?host='+str(host.hostname)+'&srv='+str(srvhost)+'&view=0&source=0&start'+str(round(start,0)).replace('0','')+'&end='+str(round(end,0)).replace('.0','')


''' Download for img and user, passd'''
file = '/usr/local/nagios/img/hosts.png'
hostsurl = requests.get(hostsurl, auth=HTTPBasicAuth('nagiosadmin','systemahje'), stream=True)
if hostsurl.status_code == 200:
    with open(file, 'wb') as f:
        hostsurl.raw.decode_content = True
        shutil.copyfileobj(hostsurl.raw, f)

if __name__ == "__main__":
    main()
    sys.exit(0)