from aiogram import Bot, types
from aiogram import types
from aiogram import *
from aiogram.types import Message, Location
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import requests
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle
from config import *
from sqlighter import SQLighter
import hashlib
import keyboards as kb
import json

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = SQLighter('dbBot.db')

class inline:
    async def CheckCoin(inline_query):
        print(inline_query)
        # id affects both preview and content,
        # so it has to be unique for each result
        # (Unique identifier for this result, 1-64 Bytes)
        # you can set your unique id's
        # but for example i'll generate it based on text because I know, that
        # only text will be passed in this example
        text = inline_query.query or 'echo'
        
        input_content = InputTextMessageContent(text)
        print(input_content)
        result_id: str = hashlib.md5(text.encode()).hexdigest()
        #headers = {
        #'accept': 'application/json'
        #}
        
        PARAM = {
            "vs_currency":'usd',
            "ids":text,
            "order":'market_cap_desc',
            "per_page":"100",
            "page":'1',
            "sparkline":"false"
        }
            
        jsons = requests.get(url="https://api.coingecko.com/api/v3/coins/markets", params=PARAM)
        jsonStatus = jsons
        if jsonStatus.status_code == 200:
            jsons = jsons.json()
            #priceCoin = str(jsons['current_price'])
            #print(priceCoin)
            #print(jsons)
            if(str(jsons) == '[]'):
                try:
                    db.coin_symbol(str(text))
                    coinID = db.coin_symbol(str(text))
                except:
                    try:
                        db.coin_name(str(text))
                        coinID = db.coin_name(str(text))
                        print(coinID)
                    except:
                        item = InlineQueryResultArticle(
                        id=result_id,
                        title=f'Похоже что такой криптовалюты нету: {text!r}',
                        input_message_content=input_content,
                        reply_markup=kb.inline_kb_TEST
                        )
                        await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1, switch_pm_parameter="perehodSinline", switch_pm_text="Перейти в бота")
                        return()
                PARAM = {
                    "vs_currency":'usd',
                    "ids":coinID,
                    "order":'market_cap_desc',
                    "per_page":"100",
                    "page":'1',
                    "sparkline":"false"
                }
                    
                jsons = requests.get(url="https://api.coingecko.com/api/v3/coins/markets", params=PARAM).json()
                '''
                item = InlineQueryResultArticle(
                    id=result_id,
                    title=f'Результат {text!r}',
                    input_message_content=input_content,
                    reply_markup=kb.inline_kb_TEST
                )
                '''
                #print(jsonsCoin)
                #print(jsonsCoin['name'])
                coin_id = str(jsons[0]['id'])
                coin_symbol = str(jsons[0]['symbol'])
                coin_name = str(jsons[0]['name'])
                coin_image = str(jsons[0]['image'])
                coin_current_price = str(jsons[0]['current_price'])
                coin_market_cap = str(jsons[0]['market_cap'])
                coin_market_cap_rank = str(jsons[0]['market_cap_rank'])
                coin_fully_diluted_valuation = str(jsons[0]['fully_diluted_valuation'])
                coin_total_volume = str(jsons[0]['total_volume'])
                coin_high_24h = str(jsons[0]['high_24h'])
                coin_low_24h = str(jsons[0]['low_24h'])
                coin_price_change_24h = str(jsons[0]['price_change_24h'])
                coin_price_change_percentage_24h = str(jsons[0]['price_change_percentage_24h'])
                coin_market_cap_change_24h = str(jsons[0]['market_cap_change_24h'])
                coin_market_cap_change_percentage_24h = str(jsons[0]['market_cap_change_percentage_24h'])
                coin_circulating_supply = str(jsons[0]['circulating_supply'])
                coin_total_supply = str(jsons[0]['total_supply'])
                coin_max_supply = str(jsons[0]['max_supply'])
                coin_ath = str(jsons[0]['ath'])
                coin_ath_change_percentage = str(jsons[0]['ath_change_percentage'])
                coin_ath_date = str(jsons[0]['ath_date'])
                coin_atl = str(jsons[0]['atl'])
                coin_atl_change_percentage = str(jsons[0]['atl_change_percentage'])
                coin_roi = str(jsons[0]['roi'])
                coin_last_updated = str(jsons[0]['last_updated'])
                #print(jsonsCoin)
                input_content = InputTextMessageContent("Название койна: <b>" + str(coin_name) + "</b>(<b>" + str(coin_symbol) + "</b>)\nТекущая цена: <b>" + str(coin_current_price) + " USD (" + str(coin_price_change_percentage_24h) + "%)</b>\nНаивысшая цена за 24 часа: <b>" + str(coin_high_24h) + "</b>\nНаименьшая цена за 24 часа: <b>" + str(coin_low_24h) + "</b>\nРыночная капитализация: <b>" + str(coin_market_cap) + "USD (" + str(coin_market_cap_change_percentage_24h) + "%)</b>\nВ списке по капитализации: <b>" + str(coin_market_cap_rank) + "</b>\nВ обращении: <b>" + str(coin_circulating_supply) + "</b>\nВсего монет: <b>" + str(coin_total_supply) + "</b>\nМаксимальное количество монет: <b>" + str(coin_max_supply) + "</b>", parse_mode=types.ParseMode.HTML)
                item = InlineQueryResultArticle(
                    id=result_id,
                    title=f'Я нашел криптовалюту: {text!r}',
                    input_message_content=input_content,
                    thumb_url=coin_image,
                    reply_markup=kb.inline_kb_TEST
                )
                await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1, switch_pm_parameter="perehodSinline", switch_pm_text="Перейти в бота")
            else:
                coin_id = str(jsons[0]['id'])
                coin_symbol = str(jsons[0]['symbol'])
                coin_name = str(jsons[0]['name'])
                coin_image = str(jsons[0]['image'])
                coin_current_price = str(jsons[0]['current_price'])
                coin_market_cap = str(jsons[0]['market_cap'])
                coin_market_cap_rank = str(jsons[0]['market_cap_rank'])
                coin_fully_diluted_valuation = str(jsons[0]['fully_diluted_valuation'])
                coin_total_volume = str(jsons[0]['total_volume'])
                coin_high_24h = str(jsons[0]['high_24h'])
                coin_low_24h = str(jsons[0]['low_24h'])
                coin_price_change_24h = str(jsons[0]['price_change_24h'])
                coin_price_change_percentage_24h = str(jsons[0]['price_change_percentage_24h'])
                coin_market_cap_change_24h = str(jsons[0]['market_cap_change_24h'])
                coin_market_cap_change_percentage_24h = str(jsons[0]['market_cap_change_percentage_24h'])
                coin_circulating_supply = str(jsons[0]['circulating_supply'])
                coin_total_supply = str(jsons[0]['total_supply'])
                coin_max_supply = str(jsons[0]['max_supply'])
                coin_ath = str(jsons[0]['ath'])
                coin_ath_change_percentage = str(jsons[0]['ath_change_percentage'])
                coin_ath_date = str(jsons[0]['ath_date'])
                coin_atl = str(jsons[0]['atl'])
                coin_atl_change_percentage = str(jsons[0]['atl_change_percentage'])
                coin_roi = str(jsons[0]['roi'])
                coin_last_updated = str(jsons[0]['last_updated'])
                #print(jsonsCoin)
                input_content = InputTextMessageContent("Название койна: <b>" + str(coin_name) + "</b>(<b>" + str(coin_symbol) + "</b>)\nТекущая цена: <b>" + str(coin_current_price) + " USD (" + str(coin_price_change_percentage_24h) + "%)</b>\nНаивысшая цена за 24 часа: <b>" + str(coin_high_24h) + "</b>\nНаименьшая цена за 24 часа: <b>" + str(coin_low_24h) + "</b>\nРыночная капитализация: <b>" + str(coin_market_cap) + "USD (" + str(coin_market_cap_change_percentage_24h) + "%)</b>\nВ списке по капитализации: <b>" + str(coin_market_cap_rank) + "</b>\nВ обращении: <b>" + str(coin_circulating_supply) + "</b>\nВсего монет: <b>" + str(coin_total_supply) + "</b>\nМаксимальное количество монет: <b>" + str(coin_max_supply) + "</b>", parse_mode=types.ParseMode.HTML)
                item = InlineQueryResultArticle(
                    id=result_id,
                    title=f'Я нашел криптовалюту: {text!r}',
                    input_message_content=input_content,
                    thumb_url=coin_image,
                    reply_markup=kb.inline_kb_TEST
                )
                await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1, switch_pm_parameter="perehodSinline", switch_pm_text="Перейти в бота")
        else:
            print(input_content)
            item = InlineQueryResultArticle(
                id=result_id,
                title=f'Сервер времено не доступен',
                input_message_content=input_content,
                reply_markup=kb.inline_kb_TEST
            )
            await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1, switch_pm_parameter="perehodSinline", switch_pm_text="Перейти в бота")