from aiogram import Bot, types
from aiogram.types import Message, Location
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
import random
import json
from bs4 import BeautifulSoup

from config import *
from layouts import *
from sqlighter import SQLighter
from telegraph import Telegraph

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = SQLighter('dbBot.db')

class VkUrlInform:
    async def VKUrl(VKid, msgID):
        telegraph = Telegraph()
        me = await bot.get_me()
        urlBot = "https://t.me/" + me.username
        bot_author = me.first_name
        bot_short_name = me.first_name
        telegraph.create_account(short_name=bot_short_name, author_name=bot_author, author_url=urlBot)
        newsfeedStatus = True
        schet = 1
        PARAMSUSERGET = {
                "user_ids":VKid,
                "fields":"bdate, crop_photo",
                "lang":VK_LANG,
                "access_token": TOKEN_VK,
                "v": VK_API
            }
            
        json = requests.get(url="https://api.vk.com/method/users.get?", params=PARAMSUSERGET).json()
        bdate = "Не указано"
        first_name = "Не указано"
        last_name = "Не указано"
        if(str(json["response"][0]).find("first_name") != -1):
            first_name = json["response"][0]["first_name"]
        if(str(json["response"][0]).find("last_name") != -1):
            last_name = json["response"][0]["last_name"]
        VKid = str(json["response"][0]["id"])
        PARAMSNEWSFEED = {
                "owner_id":VKid,
                "count":countCommentVK,
                "access_token": TOKEN_VK_USER,
                "v": VK_API
        }
        avatarVK = "none"
        if(str (json["response"][0]).find("crop_photo") != -1):
            for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                if (size['type'] == "z"):
                    avatarVK = size['url']
            
            if (avatarVK == "none"):
                for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                    if (size['type'] == "y"):
                        avatarVK = size['url']
            
            if (avatarVK == "none"):
                for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                    if (size['type'] == "x"):
                        avatarVK = size['url']
                        
            if (avatarVK == "none"):
                for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                    if (size['type'] == "w"):
                        avatarVK = size['url']
                       
            if (avatarVK == "none"):
                for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                    if (size['type'] == "s"):
                        avatarVK = size['url']
                        
            if (avatarVK == "none"):
                for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                    if (size['type'] == "r"):
                        avatarVK = size['url']
           
            if (avatarVK == "none"):
                for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                    if (size['type'] == "q"):
                        avatarVK = size['url']
                
            if (avatarVK == "none"):
                for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                    if (size['type'] == "p"):
                        avatarVK = size['url']
                        
            if (avatarVK == "none"):
                for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                    if (size['type'] == "o"):
                        avatarVK = size['url']
            
            if (avatarVK == "none"):
                for size in json["response"][0]["crop_photo"]["photo"]["sizes"]:
                    if (size['type'] == "m"):
                        avatarVK = size['url']
        
        try:
            exception = int(db.vkCheckProfileID(VKid))
        except:
            exception = 0
        
        if(str (json["response"][0]).find("bdate") != -1):
            bdate = str(json["response"][0]["bdate"])
        else:
            bdate = "Не указано"
        if(str (json["response"][0]).find("deactivated") != -1):
            req = "<b>Имя пользователя: </b>" + first_name + " " + last_name + "\n <b>ID: </b>" + VKid + "\n<b>АККАУНТ ДЕАКТИВИРОВАН</b>" + "\n <b>Упоминания пользователя: </b>https://vk.com/feed?obj=" + VKid + "&section=mentions"
            await bot.send_photo(msgID, "https://vk.com/images/deactivated_200.png", req, parse_mode=types.ParseMode.HTML)
        if(exception == 1):
            await bot.send_message(msgID, 'Пользователь предпочел скрыть информацию о себе', parse_mode=types.ParseMode.HTML)
        else:
            await bot.send_message(msgID, "Страница найдена")
            url = 'https://vk.com/foaf.php?id='+VKid
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            createdVK =  soup.find_all('ya:created')
            createdVK = str(createdVK)
            index = createdVK.split('"')
            createdVK = str(index[1])
            modifiedVK = soup.find_all('ya:modified')
            modifiedVK = str(modifiedVK)
            if(modifiedVK == "[]"):
                modifiedVK = "Вроде не редактировал"
            else:
                index = modifiedVK.split('"')
                modifiedVK = str(index[1])
            if (avatarVK == "none"):
                for link in soup.find_all('foaf:image'):
                    avatarVK = link.get('rdf:about')
            if (avatarVK == "none"):
                avatarVK = "https://vk.com/images/camera_200.png"
            request_user_id = str(VKid)
            if(not db.vkSerchProfileID(request_user_id)): #################################
                db.add_vkSerchProfileID(request_user_id)
            else:
                db.pp_vkSerchProfileID(request_user_id)
            Stat_vkSerchProfileID = str(db.Stat_vkSerchProfileID(request_user_id))[2:-3]
            requestVKComment = requests.get(url="https://api.vk.com/method/newsfeed.getMentions?", params=PARAMSNEWSFEED)
            json_VKComment = requestVKComment.json()
            post_idNewseedVK = "none"
            if(str(json_VKComment['response']['count']) == "0" or exception == 2):
                newsfeedStatus = False
                await bot.send_message(msgID, "Не удалось найти упоминиания этой страницы", parse_mode=types.ParseMode.HTML)
            else:
                telegraphtext = "<h3>Упоминания пользователя</h3>"
                for item in  json_VKComment['response']['items']:
                    from_idNewseedVk = item['to_id']
                    if(str(item).find('id') != -1 and str(item).find('id') < 150):
                        post_idNewseedVK = item['id']
                        textVK = str(item['text'])
                        comentIDTemp = "[id" + VKid + "|"
                        count = textVK.find(comentIDTemp)
                        count = count + 1
                        textVK = textVK[count::]
                        textVK = textVK.split("|")[1]
                        textVK = textVK.split("]")[0]
                        VKUrlComment = "https://vk.com/wall" + str(from_idNewseedVk) + "_" + str(post_idNewseedVK)
                        textVK = textVK + " Упоминание " + str(schet)
                        Report_VK_Newsfeed = '<p><a target="_blank" href="' + str(VKUrlComment) + '">' + textVK + '</a></p>' 
                        telegraphtext = telegraphtext + Report_VK_Newsfeed
                    else:
                        post_idNewseedVK = item['post_id']
                        text = str(item['text'])
                        VKUrlComment = "https://vk.com/wall" + str(from_idNewseedVk) + "_" + str(post_idNewseedVK)
                        textVK = str(item['text'])
                        comentIDTemp = "[id" + VKid + "|"
                        count = textVK.find(comentIDTemp)
                        count = count + 1
                        textVK = textVK[count::]
                        textVK = textVK.split("|")[1]
                        textVK = textVK.split("]")[0]
                        VKUrlComment = "https://vk.com/wall" + str(from_idNewseedVk) + "_" + str(post_idNewseedVK)
                        textVK = textVK + " Упоминание " + str(schet)
                        Report_VK_Newsfeed = '<p><a target="_blank" href="' + str(VKUrlComment) + '">' + textVK + '</a></p>' 
                        telegraphtext = telegraphtext + Report_VK_Newsfeed
                    schet = schet + 1
            telegraphStat = ""
            if(newsfeedStatus):
                response = telegraph.create_page(
                'vk-' + VKid,
                html_content=telegraphtext,
                author_name=bot_author,
                author_url=urlBot
                )
                telegraphStat = 'https://telegra.ph/{}'.format(response['path'])
            else:
                telegraphStat = "не удалось найти"
            req = "<b>Имя пользователя: </b>" + first_name + " " + last_name + "\n <b>ID: </b>" + VKid + "\n <b>День рождения: </b>" + bdate  + "\n <b>Последнее изменение страницы: </b>" + modifiedVK[:-6] + "\n <b>Дата создания страницы: </b>" + createdVK[:-6] + "\n<b>Упоминания пользователя: </b>" + str(telegraphStat) + " \n<b>Интересовались </b>" + Stat_vkSerchProfileID + "<b> раза(включая этот запрос)</b>"
            await bot.send_photo(msgID, avatarVK, req, parse_mode=types.ParseMode.HTML)
            await bot.send_message(msgID, shareBotAdv + "https://t.me/" + me.username + "?start=" + str(msgID), parse_mode=types.ParseMode.HTML)