from aiogram import Bot, types
from config import *
from sqlighter import SQLighter
from bs4 import BeautifulSoup
from layouts import *
from telegraph import Telegraph

import random
import json
import requests

bot = Bot(token=TOKEN)
db = SQLighter('dbBot.db')

class gosNumber:
    async def vin(gosNumber, msgID):
        telegraph = Telegraph()
        me = await bot.get_me()
        urlBot = "https://t.me/" + me.username
        bot_author = me.first_name
        bot_short_name = me.first_name
        telegraph.create_account(short_name=bot_short_name, author_name=bot_author, author_url=urlBot)
        noBallance = False
        noVin = "True"
        count = 0
        ##############https://vin01.ru/v2/rsaApi.php?vin=XTA210430R0446549&key=03AGdBq25krokvayKqUowiGU_HfPGREzDJJQG9r_nSvlYT_ft_kDHZf7CMRjZm_lMg0_eCM59u_QOaQztbJ_N-21HLF5JPjsNh2gmVD31EeP5wHgMpDBBC2JFvobXabz3LCoE2oy5w3mFHIeuKi1WClwVVufgUPb9SwGY1cLaPapt2LSQqkbe9t_Je09tFcOnO3KA-XZJygRhBMNy7MQjUN4nxQ53WubniNcg2VqQBX46uPF_CYgEj8H2dkFUw8A1CXESlELL8LJz6dXOsr6AtUZAcbwh6U0hwmzqOdxd3PW8qrLlq9xn6WIXpY7HnFGLpWfPOVCvFLd_DGMVxDv5uavGwGkU1NnVNBWwsHOTuDK9LjEGdJhnm0Hw6DWVfSYrQIVQcKHsCl8y-e9FpW23GMixBhbPIOFLl3xFp0jKBXuoBCcRjpgqfQmQ
        ###Проверка действующего полиса осаго
        ###################################################
        ###https://vin01.ru/api/apiSud.php?vin=XTA210430R0446549
        ###Проверка судебных решений
        url = "https://ntws.pro/widget/osago/preload"
         
        payload = json.dumps({
          "identType": 1,
          "identValue": gosNumber
        })
        headers = {
          'x-authorization': '8ae03c9f52351461be55b9cdcfcc08b42aab4598',
          'origin': 'https://eaisto.pro',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
          'x-widgetid': '17420',
          'Content-Type': 'application/json'
        }
        status = "Не указано"
        
        PARAM = {
            "gosNumber":gosNumber,
            "site":"1"
        }
        
        jsons = requests.get(url="https://vin01.ru/v2/getVin.php", params=PARAM).json()
        jsons = str(jsons)
        index = jsons.split("'")
        codeSostoyan = (str(index[4]))[2:-1]
        if(not(codeSostoyan == "200,")):
            await bot.send_message(msgID, "Отсутствуют сведения о ТС на сервере", parse_mode=types.ParseMode.HTML)
        if(codeSostoyan == "200,"):
            vin = str(index[9])
            noVin = "False"
            if (vin == "Сведения отсутствуют"):
                noVin = "True"
                response = requests.request("POST", url, headers=headers, data=payload).json()
                if(str(response).find("status") != -1):
                    status = str(response)
                else:
                    status = "Не указано"
                if(status == "{'status': False, 'message': 'Unauthorized'}"):
                    noVin = "True"
                    print("EAISTO UPDATE NADO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    await bot.send_message(msgID, "Отсутствуют сведения о ТС", parse_mode=types.ParseMode.HTML)
                else:
                    noVin = "False"
                    if (vin == ""):
                        noVin = "True"
                        await bot.send_message(msgID, "Отсутствуют сведения о ТС", parse_mode=types.ParseMode.HTML)
        if(noVin == "False"):
            await bot.send_message(msgID, "Отчет готовится, ожидайте", parse_mode=types.ParseMode.HTML)
            #await bot.send_message(msgID, "Похоже что возникла ошибка на сервере ГИБДД, проверка невозможна", parse_mode=types.ParseMode.HTML)
            #Идем Чекать
            PARAMSGIBDD = {
                "vin":vin,
                "checkType":"history"
            }
            jsons = requests.post(url="https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/history", params=PARAMSGIBDD).json()
            noData = "Нет информации в базе"
            status = str(jsons["status"])
            if(status == "200"):
                bodyNumber = noData
                engineVolume = noData
                color = noData
                year = noData
                engineNumber = noData
                model = noData
                powerHp = noData
                if(str(jsons["RequestResult"]["vehicle"]).find("engineVolume") != -1):
                    engineVolume = str(jsons["RequestResult"]["vehicle"]["engineVolume"])
                if(str(jsons["RequestResult"]["vehicle"]).find("color") != -1):
                    color = str(jsons["RequestResult"]["vehicle"]["color"])
                if(str(jsons["RequestResult"]["vehicle"]).find("bodyNumber") != -1):
                    bodyNumber = str(jsons["RequestResult"]["vehicle"]["bodyNumber"])
                if(str(jsons["RequestResult"]["vehicle"]).find("year") != -1):
                    year = str(jsons["RequestResult"]["vehicle"]["year"])
                if(str(jsons["RequestResult"]["vehicle"]).find("engineNumber") != -1):
                    engineNumber = str(jsons["RequestResult"]["vehicle"]["engineNumber"])
                if(str(jsons["RequestResult"]["vehicle"]).find("vin") != -1):
                    vin =  str(jsons["RequestResult"]["vehicle"]["vin"])
                if(str(jsons["RequestResult"]["vehicle"]).find("model") != -1):
                    model = str(jsons["RequestResult"]["vehicle"]["model"])
                if(str(jsons["RequestResult"]["vehicle"]).find("powerHp") != -1):
                    powerHp = str(jsons["RequestResult"]["vehicle"]["powerHp"])
                if(not(int(str(db.checkBallance(msgID))) > PRICE_SEARCHAUTO)):
                    vin = "*************"
                    bodyNumber = "*************"
                    engineNumber = "*************"
                    noBallance = True
                telegraphtext = """
                <h3>Сведения о ТС</h3>
                    <p><b>Модель </b>
                    """ + model + """</p>
                    <p><b>Цвет </b>
                    """ + color + """</p>
                    <p><b>Год </b>
                    """ + year + """</p>
                    <p><b>Обьем двигателя </b>
                    """ + engineVolume + """</p>
                    <p><b>Мощность двигателя(ЛС) </b>
                    """ + powerHp + """</p>
                    <p><b>Номер двигателя </b>
                    """ + engineNumber + """</p>
                    <p><b>Номер кузова </b>
                    """ + bodyNumber + """</p>
                    <p><b>VIN </b>
                    """ + vin + """</p>
                    <p><b>История владельцев: </b></p>
                """
                for item in jsons["RequestResult"]["ownershipPeriods"]["ownershipPeriod"]:
                    dateFrom = item['from']
                    if(str(item).find("to") != -1):
                        dateTo = str(item['to'])
                    else:
                        dateTo = "Не указано"
                    count = count + 1
                    if(not(noBallance)):
                        db.sub_BalanceProfile(msgID, PRICE_SEARCHAUTO)
                        telegraphtext = telegraphtext + """<p>Владелец """ + str(count) + """ C """ + str(dateFrom) + """ по """ + str(dateTo) + """</p>"""
                if(noBallance):
                    telegraphtext = telegraphtext + """<p>Было найдено """ + str(count) + """ владельцев</p> <p>Полный отчет доступен при покупке</p>"""
                
                PARAMSGIBDDDTP = {
                    "vin":vin,
                    "checkType":"aiusdtp"
                }

                jsonsdtp = requests.post(url="https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/dtp", params=PARAMSGIBDDDTP).json()
                if(str(jsonsdtp['RequestResult']['Accidents']) == '[]'):
                    telegraphtext = telegraphtext + "<p><b>Записи о ДТП не обнаружены, возможно в базе были указаны криво данные</b></p>"
                else:
                    Accidents = jsonsdtp['RequestResult']['Accidents'][0]
                    AccidentDateTime = "none"
                    if(str(Accidents).find("AccidentDateTime") != -1):
                        AccidentDateTime = Accidents['AccidentDateTime']
                    VehicleDamageState = "none"    
                    if(str(Accidents).find("VehicleDamageState") != -1):
                        VehicleDamageState = Accidents['VehicleDamageState']
                    AccidentNumber = "none"    
                    if(str(Accidents).find("AccidentNumber") != -1):
                        AccidentNumber = Accidents['AccidentNumber']
                    AccidentType = "none"    
                    if(str(Accidents).find("AccidentType") != -1):
                        AccidentType = Accidents['AccidentType']
                    DamageDestription = "none"    
                    if(str(Accidents).find("DamageDestription") != -1):
                        DamageDestription = Accidents['DamageDestription']
                    VehicleMark = "none"    
                    if(str(Accidents).find("VehicleMark") != -1):
                        VehicleMark = Accidents['VehicleMark']
                    VehicleAmount = "none"    
                    if(str(Accidents).find("VehicleAmount") != -1):
                        VehicleAmount = Accidents['VehicleAmount']
                    VehicleYear = "none"    
                    if(str(Accidents).find("VehicleYear") != -1):
                        VehicleYear = Accidents['VehicleYear']
                    AccidentPlace = "none"    
                    if(str(Accidents).find("AccidentPlace") != -1):
                        AccidentPlace = Accidents['AccidentPlace']
                    VehicleSort = "none"    
                    if(str(Accidents).find("VehicleSort") != -1):
                        VehicleSort = Accidents['VehicleSort']
                    VehicleModel = "none"    
                    if(str(Accidents).find("VehicleModel") != -1):
                        VehicleModel = Accidents['VehicleModel']
                    OwnerOkopf = "none"    
                    if(str(Accidents).find("OwnerOkopf") != -1):
                        OwnerOkopf = Accidents['OwnerOkopf']
                    RegionName = "none"    
                    if(str(Accidents).find("RegionName") != -1):
                        RegionName = Accidents['RegionName']
                    DamagePoints = "none"    
                    if(str(Accidents).find("DamagePoints") != -1):
                        DamagePoints = Accidents['DamagePoints']
                    if(noBallance):
                        telegraphtext = telegraphtext + "<p><b>Записи о ДТП найдены, подробнее доступно в платном отчете.</b></p>"
                    else:
                        telegraphtext = telegraphtext + """
                        <p><b>Информация о ДТП</b></p>
                        <p><b>Дата и время происшествия </b>
                        """ + AccidentDateTime + """</p>
                        <p><b>Тип происшествия</b>
                        """ + AccidentType + """</p>
                        <p><b>Регион происшествия</b>
                        """ + RegionName + """</p>
                        <p><b>Место происшествия</b>
                        """ + AccidentPlace + """</p>
                        <p><b>Количество автомобилей в ДТП</b>
                        """ + VehicleAmount + """</p>
                        """
                PARAMSGIBDWANTED = {
                    "vin":vin,
                    "checkType":"wanted"
                }
                jsonwanted = requests.post(url="https://xn--b1afk4ade.xn--90adear.xn--p1ai/proxy/check/auto/wanted", params=PARAMSGIBDWANTED).json()
                if(int(jsonwanted['RequestResult']['count']) != 0):
                    countWanted = int(jsonwanted['RequestResult']['count'])
                    WantedRegion = "none"    
                    if(str(jsonwanted['RequestResult']['records'][0]).find("w_reg_inic") != -1):
                        WantedRegion = jsonwanted['RequestResult']['records'][0]['w_reg_inic']
                    WantedData = "none"    
                    if(str(jsonwanted['RequestResult']['records'][0]).find("w_data_pu") != -1):
                        WantedData = jsonwanted['RequestResult']['records'][0]['w_data_pu']
                    if(noBallance):
                        telegraphtext = telegraphtext + "<p><b>Записи о розыске найдены, подробнее доступно в платном отчете.</b></p>"
                    else:
                        telegraphtext = telegraphtext + "<p><b>Историия угонов: </b></p>"
                        telegraphtext = telegraphtext + "<p>Количество записей о розыске: " + str(countWanted) + "</p><p>Дата постановки в розыск: " + str(WantedData) + "</p><p>Регион инициатора розыска: " + str(WantedRegion) + "</p>"
                else:
                    telegraphtext = telegraphtext + "Записи о розыске не найдены"
                response = telegraph.create_page(
                'auto-' + gosNumber,
                html_content=telegraphtext,
                author_name=bot_author,
                author_url=urlBot
                )
                telegraphStat = 'https://telegra.ph/{}'.format(response['path'])
                await bot.send_message(msgID, "Статья на Telegraph(beta): " + telegraphStat, parse_mode=types.ParseMode.HTML)
                me = await bot.get_me()
                await bot.send_message(msgID, shareBotAdv + "https://t.me/" + me.username + "?start=" + str(msgID), parse_mode=types.ParseMode.HTML)
            else:
                await bot.send_message(msgID, "Информация не найдена", parse_mode=types.ParseMode.HTML)

    
    async def photo(gosNumber, msgID):
        RepotName = "Report_Auto_" + str(gosNumber) + "_" + str(random.getrandbits(50)) + ".html"
        CDReport = "Report//" + RepotName
        Report = open("Report//" + RepotName, "w+")
        lenGosNumber = len(gosNumber)
        series = gosNumber[0] + gosNumber[4] + gosNumber[5]
        number = gosNumber[1] + gosNumber[2] + gosNumber[3]
        if(lenGosNumber == 8):
            region_code = gosNumber[6] + gosNumber[7]
        if(lenGosNumber == 9):
            region_code = gosNumber[6] + gosNumber[7] + gosNumber[8]
        PARAM = {
            "tokens[series]":series,
            "tokens[number]":number,
            "tokens[region_code]":region_code,
            "token":"03AGdBq26_WCsI4phUkbKAKldlp6HdUOnb505sQC5_2ybIhLXrqP3BDL2SCFS5m3et9XSZ_5U8I6BDk2P1tUu5lZ6mtvYl74SAukoq9bcbZjAs65_nlrDAroXgruHwnjNv90d31YcqxoJ7DQBhLknpNOU3em1oCVbQbv7IM0oWnysBMf8s3jLj3sNt-MWpS2C5vvIvIob-3_iB7Z80BiasDEqN3QrPtZGZ4sHGpCFEt5_ES7ytQNG_uUycOgKT_m8vCxMJOgquV5oHx4QbDmazc29_fKI8p7kkGTi_sJ_qms-wf5f8ic8U4RXukFyEowZnQhlRk9Lnr6r_n9sTvfZR1TGnBG9FCW9VAxKEtKrWaERziLzpo0rpwBuylIYgrjR2912Qcbp90oEyOX8ciLxqYVaYdHEcH_cbt7dWCwklH2JQb_dQr6dWx_BLFGwgOydqojXGpqaJXq6Q"
        }
        headers = {
        'Host': 'www.nomerogram.ru'
        }
        url = "https://www.nomerogram.ru/search/"
        jsons = requests.post(url, headers=headers, params=PARAM).json()
        redirectUrl = str(jsons["redirectUrl"])
        response = requests.get(redirectUrl)
        soup = BeautifulSoup(response.text, 'lxml')
        photo = soup.find_all('img')
        count = 0
        Report.write(header + '<p align="center">Фотографии ТС с госномером: ' + gosNumber + '</p>' + '<div display: flex justify-content: space-between>')
        status_photo = False
        for photos in photo:
            phot = (photo[count])
            phot = str(phot)
            phot = phot.replace("data-src", "src")
            if(count > 1):
                Report.write("""<a>""" + phot + """</a>""")
                status_photo = True
            count = count + 1
        
        if(status_photo):
            Report.write("</div>")
            await bot.send_message(msgID, "Фотографии ТС", parse_mode=types.ParseMode.HTML)
            Report.write(footer)
            Report.close()
            Report = open("Report//" + RepotName, "rb")
            await bot.send_document(msgID, Report)
            me = await bot.get_me()
            await bot.send_message(msgID, shareBotAdv + "https://t.me/" + me.username + "?start=" + str(msgID), parse_mode=types.ParseMode.HTML)
        else:
            await bot.send_message(msgID, "Не удалось найти фотографии ТС", parse_mode=types.ParseMode.HTML)
