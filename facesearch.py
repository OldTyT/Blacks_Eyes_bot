import sys
import base64
import random
from pprint import pprint
from aiogram import Bot, types
from aiogram.types import Message, Location
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from sqlighter import SQLighter
from jsonrpcclient import request 
from jsonrpcclient.clients.http_client import HTTPClient
from telegraph import Telegraph

from config import *
from layouts import *
from sqlighter import SQLighter

bot = Bot(token=TOKEN)
db = SQLighter('dbBot.db')

class face:
    async def searchface(PhotoName, msgID):
        telegraph = Telegraph()
        me = await bot.get_me()
        urlBot = "https://t.me/" + me.username
        bot_author = me.first_name
        bot_short_name = me.first_name
        telegraph.create_account(short_name=bot_short_name, author_name=bot_author, author_url=urlBot)
        if(int(str(db.checkBallance(msgID))) > PRICE_FACESEARCH):
            db.sub_BalanceProfile(msgID, PRICE_FACESEARCH)
            apiUrl = "https://search4faces.com/api/json-rpc/v1";
            apiKey = FACESEARCH_API;

            client = HTTPClient(apiUrl)
            client.session.headers.update({"Content-Type": "application/json-rpc","x-authorization-token": apiKey})

            response = client.request("rateLimit")
            CDPhoto = "Photo//" + PhotoName
            with open(CDPhoto, "rb") as image_file:
                data = base64.b64encode(image_file.read()).decode("ascii")
            response = client.request("detectFaces", image=data)
            detectFaces = response.data.result
            findface = str(detectFaces["faces"])
            if(findface == '[]'):
                    await bot.send_message(msgID, 'Мне не удалось найти лицо на этой фотографии', parse_mode=types.ParseMode.HTML)
            else:
                await bot.send_message(msgID, 'Я нашел лицо, ожидайте результат', parse_mode=types.ParseMode.HTML)
                for i in range(0, len(detectFaces['faces'])):
                    response = client.request("searchFace", image = detectFaces["image"], face = detectFaces["faces"][i], source = "vk_wall", results = 10, hidden = True)
                    searchFace = response.data.result
                telegraphtext = '<h3>Результаты поиска</h3>'
                for profiles in  searchFace['profiles']:
                    score = profiles['score']
                    profile = profiles['profile']
                    photoNetwork = profiles['photo']
                    photoSource = profiles['source']
                    age = profiles['age']
                    if(str(age) == '-1'):
                        age = "Не указано"
                    first_name = profiles['first_name']
                    last_name = profiles['last_name']
                    telegraphtext = telegraphtext + '''
                    <p><a target="_blank" href="''' + str(profile) + '''"><img src="''' + str(photoSource) +'''"></a></p>
                    <p></p>
                    <p><a target="_blank" href="''' + str(profile) + '''">'''+ str(first_name) + ''' '''+ str(last_name) +'''</a></p>
                    <p>Возраст: ''' + str(age) +'''</p>
                    <p>Процент совпадения: ''' + str(score) +'''</p>
                    <p><a target="_blank" href="''' + str(photoNetwork) +'''">Ссылка на фото в соц. сети</a></p>
                    <p>_________________</p>
                    '''
                response = telegraph.create_page(
                "Поиск по лицу",
                html_content=telegraphtext,
                author_name=bot_author,
                author_url=urlBot
                )
                telegraphStat = 'https://telegra.ph/{}'.format(response['path'])
                await bot.send_message(msgID, "Отчет на Telegraph(beta): " + telegraphStat, parse_mode=types.ParseMode.HTML)
                await bot.send_message(msgID, shareBotAdv + "https://t.me/" + me.username + "?start=" + str(msgID), parse_mode=types.ParseMode.HTML)
        else:
            balance = str(db.checkBallance(msgID))
            await bot.send_message(msgID, "Необходимо на балансе " + str(PRICE_FACESEARCH) + " рубля у вас " + balance + " рублей на балансе\nПополните баланс командой: <b>/pay сумма</b>\nУзнать свой баланс можно /profile", parse_mode=types.ParseMode.HTML)