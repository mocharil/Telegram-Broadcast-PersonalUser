from telethon import TelegramClient, sync, events
from telethon.tl.types import PeerChat, InputPeerChat
import datetime
import threading
import subprocess as sp
import time
import pandas as pd
import re,sys
import os
import schedule 
import time 
print('ready broadcast')


def run_continuously(schedule, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run
    
def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
    import subprocess as sp

    print('\n\n====================== RESTART PROGRAM ======================= ')
    time.sleep(1)
    sp.call('cls',shell=True)
    os.execv(sys.executable, ['python'] + sys.argv)


def make_login(name):
    with open('login_{}.txt'.format(name), 'w+') as f:
        api_id=input('api_id: ')
        api_hash=input('api_hash: ')
        phone_number=input('phone_number: +62')
        f.write("api_id: "+api_id+'\n')
        f.write("api_hash: "+api_hash+'\n')
        f.write("phone_number: +62"+phone_number+'\n')
        
def update_login(name):
    with open('login_{}.txt'.format(name), 'w') as f:
        api_id=input('api_id: ')
        api_hash=input('api_hash: ')
        phone_number=input('phone_number: +62')
        f.write("api_id: "+api_id+'\n')
        f.write("api_hash: "+api_hash+'\n')
        f.write("phone_number: +62"+phone_number+'\n')
        
list_txt=[]
path_inti=os.getcwd()
name=__file__
if len(name.split('\\'))>1:
    name=name.split('\\')[1]
name=name.replace('.py','')


file = 'login_{}.txt'.format(name)        
if os.path.isfile(file):
    print('you are logged in as {}'.format(name))
    
else :
    print('\nwelcome {}\n'.format(name))
    make_login(name)
    print('\nyour data has saved {}\n'.format(name))

data=open('login_{}.txt'.format(name)).read().split('\n')

#data login
for i in data:
    if 'api_id' in i:
        api_id=int(i.replace('api_id: ','')) 
    if 'api_hash' in i:
        api_hash=str(i.replace('api_hash: ','')) 
    if 'phone_number' in i:
        phone=str(i.replace('phone_number: ','')) 
        
print('waiting to logged in...')     
client = TelegramClient(name, api_id, api_hash)
client.start(phone)
import json
sp.call('cls',shell=True)
print('=======================LOGIN SUCCESS=====================================')

message=''

def make_dir(path):
    try:
        os.mkdir(path)
    except:
        pass

path_inti=os.getcwd()
path_name=path_inti+'\\'+name
make_dir(path_name)
make_dir(path_name+'\\photo')
def kirim():
    date_now=datetime.datetime.now()
    if int(str(date_now)[10:13])>=8:
        try:
            with open(path_name+'\\posting_{}.json'.format(name)) as f:
                message=json.load(f)['message']
            if len(os.listdir(path_name+'\\photo'))==0:
                o=client.get_dialogs()
                list_group=[]
                for i in o:
                    if i.is_group:
                        title=i.entity.title
                        title=title.lower()
                        try:
                            if 'tes' in title:
                                client.send_message(i.id, message)
                                print('pesan terkirim ke grup {}'.format(title))
                        except Exception as e:
                            print('update pesan anda ke telegram @@broadcast_telegram_bot')
                            
            else :
                photos=[ path_name+'\\photo\\'+i  for i in os.listdir(path_name+'\\photo')]
                o=client.get_dialogs()
                list_group=[]
                for i in o:
                    if i.is_group:
                        title=i.entity.title
                        title=title.lower()
                        try:
                            if 'tes' in title:
                                client.send_file(i.id, photos, caption=message[:1000])
                                print('pesan terkirim ke grup {} disertai dengan foto'.format(title))
                        except Exception as e:
                            print(e)      
        except:
            pass

if os.path.isfile(path_name+'\\posting_{}.json'.format(name))==False:
    print('update pesan anda di akun bot telegram')
    with open(path_name+'\\posting_{}.json'.format(name),'w') as f:
        json.dump({'message':message,'time':'60','username':name},f)

def error():
    try:
        open(path_name+'\\runner.txt').read()
    except Exception as e:
        kirim()
        time.sleep(5)
        open(path_name+'\\runner.txt').read()
##=====================restart=========================
schedule.clear()
schedule.every(60).minutes.do(restart_program)
run_continuously(schedule)
with open(path_name+'\\runner.txt', 'w') as f:
    f.write('Yes')
        
p=False
while True:
    sp.call('cls',shell=True)
    print('======================= {} =================================='.format(name.upper()))
    try:
        open(path_name+'\\runner.txt').read()   
    except Exception as e:
        print('pesan telah terupdate dan dikirim ke semua group')
    
    with open(path_name+'\\posting_{}.json'.format(name)) as f:
        data=json.load(f)
    message=data['message']
    timez=data['time']
    
    with open(path_name+'\\runner.txt', 'w') as f:
        f.write('Yes')

    
    schedule.every(int(timez)).minutes.do(kirim).tag('kirim')
    schedule.every(1).seconds.do(error).tag('error')
    while True:
        try:
            schedule.run_pending()
        except KeyboardInterrupt:
            p = True
            break
        except FileNotFoundError:
            schedule.clear('kirim')
            schedule.clear('error')
            sp.call('cls',shell=True)
            print('======================= {} =================================='.format(name.upper()))
            break
            
    if p==True:
        break
client.disconnect()
print('disconect')
