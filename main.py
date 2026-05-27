import telebot
import time
from datetime import datetime

from config import *
from pageUpdate import *

bot = telebot.TeleBot(token, parse_mode='html')

statisticsMsg = """<b>⚡️ Parser launched!</b>
➖➖➖➖➖➖➖➖➖➖
⏰ Session started: <code>{}</code>

✉️ Requests sent: <code>{}</code>
✅ Successful requests: <code>{}</code>
❌ Errors: <code>{}</code>
"""

@bot.message_handler(commands=['start'])
def start(message):
    
    print('Starting the parser bot...')

    if message.from_user.id == admin:
        now = datetime.now()
        dtString = now.strftime("%d/%m/%Y %H:%M:%S")
        
        sendTotal, successTotal,errorsTotal = 0, 0, 0
        msg = bot.send_message(admin,"<b>Parser is launching...</b>") 
        parser = ProductParser()

        productStatus = False

        while True:
            try:
                result = parser.check()

                if result:
                    successTotal += 1
                    if not productStatus:
                        print('[+] Successful request')
                        bot.send_message(admin,'<b>Product list changes detected!</b>✅')
                        productStatus = True

                else:
                   if productStatus:
                       bot.send_message(admin,'<b>Product list is empty again</b> ⏳')
                       productStatus = False

                   print('[-] No products found')

            except BrowserError as e:
                errorsTotal += 1
                time.sleep(30)
                print('[!] Error occured') 
            
            finally:
                sendTotal += 1

                print('[*] Request completed')

                bot.edit_message_text(
                    statisticsMsg.format(dtString,sendTotal,successTotal,errorsTotal),
                    msg.chat.id,
                    msg.id
                )    

            time.sleep(1)

bot.infinity_polling()