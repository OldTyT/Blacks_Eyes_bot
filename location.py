from aiogram import Bot, types
from aiogram.types import Message, Location
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
import json
import random
from aiogram.types import InputFile
from config import *
from sqlighter import SQLighter
from layouts import *
from telegraph import Telegraph

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = SQLighter('dbBot.db')

class geolocationvksearch:
    async def locationVKPhoto(longitude, latitude, user_id):
        telegraph = Telegraph()
        me = await bot.get_me()
        urlBot = "https://t.me/" + me.username
        bot_author = me.first_name
        bot_short_name = me.first_name
        telegraph.create_account(short_name=bot_short_name, author_name=bot_author, author_url=urlBot)
        urlPhotoVK = "none"
        RepotName = "Report_" + str(random.getrandbits(50)) + ".html"
        CDReport = "Report//" + RepotName
        Report = open("Report//" + RepotName, "w+")

        Report.write(header + """
<div display: flex justify-content: space-between>
                    """)

        PARAMS = {
                "lat":latitude,
                "long":longitude,
                "sort":sortPhotoVK,
                "radius":radiusPhotoSearch,
                "count": countGEOVk,
                "access_token": TOKEN_VK_USER,
                "v": VK_API
            }
        requestVKPhoto = requests.get(url="https://api.vk.com/method/photos.search", params=PARAMS)
        json_VKPhoto = requestVKPhoto.json()

        qqq = "<h3>Фотографии рядом с геопозицией</h3>"
        
        for item in  json_VKPhoto['response']['items']:
            #item['album_id']
            idPhotoVk = item['id']
            ownerIDPhoto = item['owner_id']
            VKUrlPhoto = "https://vk.com/photo" + str(ownerIDPhoto) + "_" + str(idPhotoVk)
            for size in item['sizes']:
                typePhoto = size['type']
                if (typePhoto == "x"):
                    urlPhotoVK = size['url']
                    Report_VK_Photo = '<a target="_blank" href="' + VKUrlPhoto + '"><img style="margin: 10px; border-radius: 10px;" src="' + urlPhotoVK + '" alt=""></a>'
                    qqq = qqq + str(Report_VK_Photo)
                    Report.write(Report_VK_Photo)
                else:
                    qqq = qqq
                    urlPhotoVK = "none"
        response = telegraph.create_page(
                'geo-' + str(random.getrandbits(50)),
                html_content=qqq,
                author_name=bot_author,
                author_url=urlBot
        )
        telegraphStat = 'https://telegra.ph/{}'.format(response['path'])
        await bot.send_message(user_id, "Отчет на Telegraph(beta): " + telegraphStat, parse_mode=types.ParseMode.HTML)
        Report.write(footer)
        Report.close()
        Report = open("Report//" + RepotName, "rb")
        await bot.send_document(user_id, Report)
        me = await bot.get_me()
        await bot.send_message(user_id, shareBotAdv + "https://t.me/" + me.username + "?start=" + str(user_id), parse_mode=types.ParseMode.HTML)