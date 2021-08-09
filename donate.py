import requests
import random
import json

from config import *

from aiogram import Bot, types
from aiogram.types import Message, Location
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sqlighter import SQLighter

import requests
import random
import json

bot = Bot(token=TOKEN)

db = SQLighter('dbBot.db')

class pay:
    async def donate(msgID, price):
        price = int(price)
        comment = random.getrandbits(50)
        await bot.send_message(msgID, "Переведите <code>" + str(price) + "</code> рублей на счет " + CHECK_QIWI + " с комментарием <code>" + str(comment) + "</code>", parse_mode=types.ParseMode.HTML)
        db.addCommentPay(msgID, comment, price)
        
    async def payments(msgID):
        comment = str(db.checkCommentPay(msgID))
        price = str(db.checkPricePay(msgID))
        if (not(comment == "none" and price == "none")):
            count = 0
            s = requests.Session()
            s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN  
            parameters = {'rows': '50'}
            h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+ QIWI_ACCOUNT +'/payments', params = parameters)
            req = json.loads(h.text)
            for i in range(len(req['data'])):
                if str(req['data'][i]['comment']) == comment:
                    if str(req['data'][i]['sum']['amount']) == price:
                        count = 1
            if (count == 1):
                await bot.send_message(msgID, "<b>Платеж прошел!</b>\nНа сумму <code>" + str(price) + "</code> рублей с коментарием <code>" + str(comment) + "</code>", parse_mode=types.ParseMode.HTML)
                db.add_BalanceProfile(msgID, price)
                comment = "none"
                price = "none"
                db.addCommentPay(msgID, comment, price)
            else:
                await bot.send_message(msgID, "<b>Платеж не прошел!</b>\nНа сумму <code>" + str(price) + "</code> рублей с коментарием <code>" + str(comment) + "</code>", parse_mode=types.ParseMode.HTML)
        else:
            await bot.send_message(msgID, "<b>Платеж не был создан!</b>\nВоспользуйтесь командой /pay сумма_платежа\nПример: <b>/pay 50</b>", parse_mode=types.ParseMode.HTML)