import os
import json,re
import sys
import time
import psutil
import logging
import subprocess as sp

import schedule
import threading, datetime
from telegram.ext import CommandHandler,Filters, Updater

sp.call('cls',shell=True)
print('\n================BOT READY=================')
print('ketik: /post untuk mengganti pesan yang akan di posting')
print('ketik: /help untuk bantuan')

def make_dir(path):
    try:
        os.mkdir(path)
    except :
        pass
path = os.getcwd()


        
def posting(bot, update):
    text=update.message.text.split(None,1)[-1]
    d=text.replace('<username>','||||').replace('<pesan>','||||').replace('<waktu>','||||').split('||||')
    if len(d)==4:
        name=d[1].replace(' ','')
        message=d[2]
        time=d[3].replace(' ','')
    else:
        name=d[0].replace(' ','')
        message=d[1]
        time=d[2].replace(' ','')
        
    print('\n==============================================')
    print('username: '+name)
    print('\n==============================================')
    print('pesan: '+message)
    print('\n==============================================')
    print('waktu kirim: '+time)
       
    path1=path+'\\{}\\'.format(name)
    make_dir(path1)
    make_dir(path1+'photo')
    import datetime
    with open(path1+'posting_{}.json'.format(name),'w') as f:
        json.dump({'message':message,'time':time,'username':name,'update':str(datetime.datetime.now())},f)
    try:
        os.remove(path1+'runner.txt')
    except:
        pass  
 
    update.message.reply_text('postingan telah terupdate menjadi :\nnama pengirim : {}'.format(name))
    update.message.reply_text('\npesan: {}'.format(message)) 
    update.message.reply_text('\nwaktu kirim: tiap {} menit'.format(time))
    
def status(bot, update):
    print('\n=======================status saat ini===========================')
    for name in os.listdir():
        try:
            for i in os.listdir(path+'/'+name):
                if '.json' in i:
                    with open(path+'/'+name+'/'+i) as f:
                        data=json.load(f) 
                    update.message.reply_text('Pesan yang dikirim:\n{}'.format(data))
        except:
            pass
 
        
    
    
def help(bot, update):
    print('\n=======================help===========================')
    t1='untuk menganti pesan yang akan dikirim, ketik dengan format :\n/post <username> username anda <pesan> pesan yang akan dikirim <waktu> waktu kirim tiap menit'
    print(t1)
    t2='contoh :\n/post <username> botak <pesan> selamat malam semua .. <waktu> 10'
    print(t2)
    t3='maka akun botak akan mengirim pesan "selamat malam semua .. " setiap 10 menit'
    print(t3)
    
    update.message.reply_text(t1)  
    update.message.reply_text(t2)
    update.message.reply_text(t3)
    
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
    
def main():

    TOKEN="your token telegram bot"
    
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('post',posting,filters=Filters.private))

    dp.add_handler(CommandHandler('help',help,filters=Filters.private))
    
    dp.add_handler(CommandHandler('status',status,filters=Filters.private))

    updater.start_polling()
  
    updater.idle()
    
def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """
   

    print('\n\n====================== RESTART PROGRAM ======================= ')
    time.sleep(1)
    sp.call('cls',shell=True)
    os.execv(sys.executable, ['python'] + sys.argv)


if __name__ == '__main__':  
    
    schedule.clear()
    schedule.every(30).minutes.do(restart_program)
    run_continuously(schedule)
    main()
    
    
