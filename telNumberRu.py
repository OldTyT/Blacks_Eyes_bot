from aiogram import Bot, types
from aiogram import types
from aiogram import *
from aiogram.types import Message, Location
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from bs4 import BeautifulSoup
import json
import requests
from config import *
from sqlighter import SQLighter

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = SQLighter('dbBot.db')

class telNumberRu:
    async def info(number, msgID):
        numberDB = "7" + number
        if(not(db.phone_exists(numberDB))):
            db.add_phone(numberDB)
        else:
            db.pp_Phone(numberDB)
        url = 'https://xn----dtbofgvdd5ah.xn--p1ai/' + number + '/'
        response = requests.get(url)
        if(response.status_code == 200):
            soup = BeautifulSoup(response.text, 'lxml')
            temp =  soup.find_all("div", "tel")
            temp = str(temp)[1:-1]  
            soupTemp = BeautifulSoup(temp, 'lxml')
            sup = str(soupTemp.get_text())
            index = sup.split(': ')
            codeCountry = str(index[1].split(',')[0])
            country = str(index[2].split(',')[0])
            region = str(index[3].split(',')[0])
            operator = str(index[4].split(',')[0])
            typeNumber = str(index[5].split(',')[0])
            url = 'https://xn----dtbofgvdd5ah.xn--p1ai/php/mnp.php?nomer=7' + number
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            MNPTemp = str(soup.get_text())
            MNP = ""
            if(MNPTemp.find("no")):
                MNP = "Номер не переносился"
            if(not(MNPTemp.find("no"))):
                MNP = "Номер переносился"
            otvet = """
Номер телефона: <code>+7""" + str(number) + """</code>
Код страны: <code>""" + codeCountry + """</code>
Страна: <code>""" + country + """</code>
Оператор: <code>""" + operator + """</code>
Тип номера: <code>""" + typeNumber + """</code>
Регион: <code>""" + region + """</code>
Переносился ли номер: <code>""" + MNP + """</code>
Запросов по этому номеру было: <code>""" + str(db.checkRequestsPhone(numberDB)) + """</code> (включая текущий)
            """
            await bot.send_message(msgID, otvet, parse_mode=types.ParseMode.HTML)
            me = await bot.get_me()
            await bot.send_message(msgID, shareBotAdv + "https://t.me/" + me.username + "?start=" + str(msgID), parse_mode=types.ParseMode.HTML)
        else:
            await bot.send_message(msgID, "Возникла ошибка на сервере, возможно не правильно указан номер телефона", parse_mode=types.ParseMode.HTML)