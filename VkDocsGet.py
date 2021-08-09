from aiogram import Bot, types
from aiogram.types import Message, Location
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from telegraph import Telegraph
import requests
import random
import json

from config import *
from layouts import *
from sqlighter import SQLighter

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = SQLighter('dbBot.db')


class VkDocs:
    async def VkDocsGet(msgID, name_file):
        telegraph = Telegraph()
        me = await bot.get_me()
        urlBot = "https://t.me/" + me.username
        bot_author = me.first_name
        bot_short_name = me.first_name
        telegraph.create_account(short_name=bot_short_name, author_name=bot_author, author_url=urlBot)
        PARAMS = {
                "q":name_file,
                "search_own":"0",
                "count":countVkDocs,
                "access_token": TOKEN_VK_USER,
                "v": VK_API
            }
        jsons = requests.get(url="https://api.vk.com/method/docs.search", params=PARAMS).json()
        if(str(jsons['response']['count']) == "0"):
            await bot.send_message(msgID, "Не удалось найти документы по заданому запросу", parse_mode=types.ParseMode.HTML)
        else:
            telegraphtext = "<h3>Вот список найденых документов</h3>"
            file_count = 1
            for item in  jsons['response']['items']:
                owner_id = item['owner_id']
                title = item['title']
                ext = item['ext']
                vkDocsUrl = item['url']
                if(str(vkDocsUrl).find("-") != -1):
                    owner_id = str(owner_id)[1::]
                    telegraphtext = telegraphtext + '<p><b>Файл номер: </b>' + str(file_count) + '</p><p><b>Расширение файла: </b>' + str(ext) + '</p><p><a target="_blank" href="https://vk.com/club' + str(owner_id) + '">Залил паблик</a></p><p><a target="_blank" href="' + str(vkDocsUrl) + '">' + str(title) + '</a></p><p>________________________</p>'
                    file_count = file_count + 1
                else:
                    telegraphtext = telegraphtext + '<p><b>Файл номер: </b>' + str(file_count) + '</p><p><b>Расширение файла: </b>' + str(ext) + '</p><p><a target="_blank" href=https://vk.com/id' + str(owner_id) + '>Залил юзер</a></p><p><a target="_blank" href="' + str(vkDocsUrl) + '">' + str(title) + '</a></p><p>________________________</p>'
                    file_count = file_count + 1
            response = telegraph.create_page(
            name_file,
            html_content=telegraphtext,
            author_name=bot_author,
            author_url=urlBot
            )
            telegraphStat = 'https://telegra.ph/{}'.format(response['path'])
            await bot.send_message(msgID, "Отчет на Telegraph(beta): " + telegraphStat, parse_mode=types.ParseMode.HTML)
            await bot.send_message(msgID, shareBotAdv + "https://t.me/" + me.username + "?start=" + str(msgID), parse_mode=types.ParseMode.HTML)