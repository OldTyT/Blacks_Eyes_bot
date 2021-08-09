import sqlite3
from dateNow import *

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))
            
    def add_subscriber(self, user_id, first_name, last_name, username, request_user_buy = dateNow.dateTime(), reg_user_data = dateNow.dateTime(), last_msg_datatime = dateNow.dateTime(), pro_user_data = dateNow.dateTime()):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `username`, `request_user_buy`, `reg_user_data`, `last_msg_datatime`, `pro_user_data`) VALUES(?,?,?,?,?,?,?,?)", (user_id,first_name,last_name,username,request_user_buy,reg_user_data,last_msg_datatime,pro_user_data))
    
    def select_all_users(self,):
        """Получаем все ID пользователей телеграм в нешей базе"""
        with self.connection:
            result = self.cursor.execute("SELECT `user_id` FROM  `users`").fetchall()
            return(result)
            
    def privilege(self, user_id, privilege):
        """Проверяем уровень доступа юзера"""
        with self.connection:
            result = self.cursor.execute("SELECT `privilege` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            result = result[0]
            if(int(result) >= privilege):
                result = True
            else:
                result = False
            return(result)
            
    def blockUserCheck(self, user_id):
        """Проверяем блокировку юзера"""
        with self.connection:
            result = self.cursor.execute("SELECT `block_user` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()[0]
            return(result)
            
    def banUser(self, user_id):
        """Баним юзера нахуй"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `block_user` = 1 WHERE `user_id` = ?", (user_id,))
            
    def spamUser(self, user_id, spamSMS):
        """Обновляем спам юзера"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `sms_spam` = `sms_spam`+1 WHERE `user_id` = ?", (user_id,))
            result = self.cursor.execute("SELECT `sms_spam` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()[0]
            spam = False
            if(int(result) >= spamSMS):
                self.cursor.execute("UPDATE `users` SET `block_user` = 1 WHERE `user_id` = ?", (user_id,))
                spam = True
            return(spam)
                
    def NoSpamUser(self, user_id):
        """Обновляем спам юзера"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `sms_spam` = 0 WHERE `user_id` = ?", (user_id,))
            
    def countLine(self):
        """Получаем количество строк в таблице"""
        with self.connection:
            result = self.cursor.execute("SELECT Count(*) FROM users").fetchone()[0]
            return(result)
            
    def username(self, user_id, first_name, last_name, username):
        """Обновляем количество рефералов у юзера"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `first_name` = ?, `last_name` = ?, `username` = ? WHERE `user_id` = ?", (first_name, last_name, username, user_id))
            
            ###################################################################################################################################################
            """История сообщений"""
            
    def add_historyMSG(self, user_id, text, message, data = dateNow.dateTime()):
        """Добавляем сообщение"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `history` (`user_id`, `text`, `data`, `message`) VALUES(?,?,?,?)", (user_id, text, data, str(message)))
            
            ###################################################################################################################################################
            """Пожелания"""
            
    def add_wish(self, user_id, text):
        """Добавляем новое пожелание"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `wish` (`user_id`, `text`) VALUES(?,?)", (user_id, text))
            
    def get_wishID(self):
        """Получаем ID пожелания"""
        with self.connection:
            result = self.cursor.execute("SELECT `id` FROM `wish` WHERE rowid=last_insert_rowid()").fetchone()[0]
            return(result)
            
    def get_wishUserID(self, id):
        """Получаем пользователя пожелания"""
        with self.connection:
            result = self.cursor.execute("SELECT `user_id` FROM `wish` WHERE `id` = ?", (id,)).fetchone()[0]
            return(result)
            
    def get_wishText(self, id):
        """Получаем текс пожелания"""
        with self.connection:
            result = self.cursor.execute("SELECT `text` FROM `wish` WHERE `id` = ?", (id,)).fetchone()[0]
            return(result)
            
            ###################################################################################################################################################
            """Номера телефона"""
            
    def phone_exists(self, phone):
        """Проверяем, есть ли уже номер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `phoneNumber` WHERE `Number` = ?', (phone,)).fetchall()
            return bool(len(result))
            
    def add_phone(self, phone, requests = "1"):
        """Добавляем новый номер"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `phoneNumber` (`Number`, `requests_all`) VALUES(?,?)", (phone, requests))
            
#            def add_vkSerchProfileID(self, request_user_id, requests = "1"):
#        """Добавляем новый профиль ВК в нашу базу"""
#        with self.connection:
#            result = self.cursor.execute("INSERT INTO `vk_search` (`request_user_id`, `requests`) VALUES(?,?)", (request_user_id, requests))
            
    def checkRequestsPhone(self, phone):
        """Получаем количество поисков по номеру телефона"""
        with self.connection:
            result = self.cursor.execute("SELECT `requests_all` FROM `phoneNumber` WHERE `Number` = ?", (phone,)).fetchone()[0]
            return(result)
            
    def pp_Phone(self, phone):
        """Обновляем количество запросов профиля в ВК"""
        with self.connection:
            self.cursor.execute("UPDATE `phoneNumber` SET `requests_all` = `requests_all`+1 WHERE `Number` = ?", (phone,))
            
            ###################################################################################################################################################
            """Чат"""
    def chatUserIdCheck(self, chatUserId):
        """Проверяем ID чата"""
        with self.connection:
            result = self.cursor.execute("SELECT `chatUserId` FROM  `users` WHERE `user_id` = ?", (chatUserId,)).fetchone()[0]
            return(result)
            
            
    def chatUserIdStart(self, user_id, chatUserId):
        """Создаем чат"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `chatAllow` = 1 WHERE `user_id` = ?", (user_id,))
            self.cursor.execute("UPDATE `users` SET `chatUserId` = ? WHERE `user_id` = ?", (user_id, chatUserId,))
            self.cursor.execute("UPDATE `users` SET `chatUserId` = ? WHERE `user_id` = ?", (chatUserId, user_id,))
            
    def chatUserIdVerify(self, user_id):
        """Начинаем чат"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `chatStatus` = ? WHERE `user_id` = ?", (1, user_id,))
            result = self.cursor.execute("SELECT `chatUserId` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()[0]
            self.cursor.execute("UPDATE `users` SET `chatStatus` = ? WHERE `user_id` = ?", (1, result,))
            return(result)
            
    def chatStatusCheck(self, chatUserId):
        """Проверяем статус чата"""
        with self.connection:
            result = self.cursor.execute("SELECT `chatStatus` FROM  `users` WHERE `user_id` = ?", (chatUserId,)).fetchone()[0]
            return(result)


    def chatStatusAllowCheck(self, chatUserId):
        """Получаем Allow"""
        with self.connection:
            result = self.cursor.execute("SELECT `chatAllow` FROM `users` WHERE `user_id` = ?", (chatUserId,)).fetchone()[0]
            return(result)


    def DeleteUsersChat(self, chatUserId):
        """Удаляем чат"""
        with self.connection:
            chatUserIdTwo = self.cursor.execute("SELECT `chatUserId` FROM  `users` WHERE `user_id` = ?", (chatUserId,)).fetchone()[0]
            self.cursor.execute("UPDATE `users` SET `chatUserId` = 0, `chatStatus` = 0, `chatAllow` = 0  WHERE `user_id` = ?", (chatUserId,))
            self.cursor.execute("UPDATE `users` SET `chatUserId` = 0, `chatStatus` = 0, `chatAllow` = 0  WHERE `user_id` = ?", (chatUserIdTwo,))
            return(chatUserIdTwo)
            
            
    def chatRandom(self, Id, user_id):
        """Рандомный чат поиск"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET  `chatAllow` = 1 WHERE `user_id` = ?", (user_id,))
            result = self.cursor.execute("SELECT `chatAllow` FROM  `users` WHERE `id` = ?", (Id,)).fetchone()[0]
            if(result == 1):
                status = False
                result = self.cursor.execute("SELECT `chatUserId` FROM  `users` WHERE `id` = ?", (Id,)).fetchone()[0]
                if(result == 0):
                    status = False
                    result = self.cursor.execute("SELECT `chatStatus` FROM  `users` WHERE `id` = ?", (Id,)).fetchone()[0]
                    if(result == 0):
                        status = False
                        result = self.cursor.execute("SELECT `user_id` FROM  `users` WHERE `id` = ?", (Id,)).fetchone()[0]
                        if(str(result) == str(user_id)):
                            status = False
                        else:
                            status = True
                            self.cursor.execute("UPDATE `users` SET `chatUserId` = ?, `chatStatus` = 1  WHERE `id` = ?", (user_id, Id))
                            userTwo = self.cursor.execute("SELECT `user_id` FROM `users`  WHERE `id` = ?", (Id,)).fetchone()[0]
                            self.cursor.execute("UPDATE `users` SET `chatUserId` = ?, `chatStatus` = 1  WHERE `user_id` = ?", (userTwo, user_id))
                            return(True)
            return(False)
            ###################################################################################################################################################
            """РефералОчка"""
            ###################################################################################################################################################
    def pp_referalID(self, user_id):
        """Обновляем количество рефералов у юзера"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `referrals_attracted` = `referrals_attracted`+1 WHERE `user_id` = ?", (user_id,))
            
    def referalIDwho(self, referal, msgID):
        """Обновляем количество рефералов у юзера"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `whose_referral` = ? WHERE `user_id` = ?", (referal, msgID))
            
    def stat_referalID(self, user_id):
        """Получаем статистику рефералов"""
        with self.connection:
            result = self.cursor.execute("SELECT `referrals_attracted` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            return(result)
            
            """ВК"""
            ###################################################################################################################################################
    def vkSerchProfileID(self, request_user_id):
        """Проверяем профиль ВК в нешей базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `vk_search` WHERE `request_user_id` = ?', (request_user_id,)).fetchall()
            return bool(len(result))                

    def add_vkSerchProfileID(self, request_user_id, requests = "1"):
        """Добавляем новый профиль ВК в нашу базу"""
        with self.connection:
            result = self.cursor.execute("INSERT INTO `vk_search` (`request_user_id`, `requests`) VALUES(?,?)", (request_user_id, requests))
            
    def pp_vkSerchProfileID(self, request_user_id):
        """Обновляем количество запросов профиля в ВК"""
        with self.connection:
            self.cursor.execute("UPDATE `vk_search` SET `requests` = `requests`+1 WHERE `request_user_id` = ?", (request_user_id,))
            
    def Stat_vkSerchProfileID(self, request_user_id):
        """Получаем статистику профиля в ВК в нашей базе"""
        with self.connection:
            result = self.cursor.execute("SELECT `requests` FROM  `vk_search` WHERE `request_user_id` = ?", (request_user_id,)).fetchone()
            return(result)
            
    def vkCheckProfileID(self, request_user_id):
        """Узнаем уровень исключений юзера"""
        with self.connection:
            result = self.cursor.execute("SELECT `exception` FROM  `vk_search` WHERE `request_user_id` = ?", (request_user_id,)).fetchone()
            return(result[0])
            ###################################################################################################################################################
            
            """Пробив по номеру машины"""
            

            ###################################################################################################################################################
            
            """Статистика"""
            ###################################################################################################################################################
    def Stat_ProfileTimeReg(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `reg_user_data` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()[0]
            return(result)

    def Stat_ProfileRequestAll(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `request_user_all` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            return(result)
            
            """Обновляем время последнего сообщения"""
    def data_last_msg(self, user_id):
        with self.connection:
            dateTime = dateNow.dateTime()
            self.cursor.execute("UPDATE `users` SET `last_msg_datatime` = ? WHERE `user_id` = ?", (dateTime,user_id))
           
            
            """Получаем время последнего сообщения"""
    def Stat_last_msg(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `last_msg_datatime` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()
            return(result)
            
            
            """Обновляем количество общих запросов"""
    def request_user_all(self, user_id):
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `request_user_all` = `request_user_all`+1 WHERE `user_id` = ?", (user_id,))
            
            """Платежка"""
            ###################################################################################################################################################
            """Добавляем коментарий платежа и сумму"""                          #pay
    def addCommentPay(self, user_id, comment, price):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `comment_pay` = ?, `price_pay` = ? WHERE `user_id` = ?", (comment, price, user_id))
            
    def add_BalanceProfile(self, user_id, price):
        """Добавляем баланс юзера"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `balance` = `balance` + ? WHERE `user_id` = ?", (price, user_id))
            
    def sub_BalanceProfile(self, user_id, price):
        """Убавляем баланс юзера"""
        with self.connection:
            self.cursor.execute("UPDATE `users` SET `balance` = `balance` - ? WHERE `user_id` = ?", (price, user_id))
            
    def checkBallance(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `balance` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()[0]
            return(result)

    def checkPricePay(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `price_pay` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()[0]
            return(result)
            
    def checkCommentPay(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `comment_pay` FROM  `users` WHERE `user_id` = ?", (user_id,)).fetchone()[0]
            return(result)
            ###################################################################################################################################################
            '''Коины'''
    def add_coin(self, coinsID, coins_symbol, coins_name):
        """Добавляем список коинов"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `coinTables` (`id`, `symbol`, `name`) VALUES(?,?,?)", (coinsID, coins_symbol, coins_name))
            
    def coin_name(self, text):
        """Узнаем ID Коина"""
        with self.connection:
            result = self.cursor.execute("SELECT `id` FROM  `coinTables` WHERE `name` = ?", (text,)).fetchone()
            return(result[0])
            
    def coin_symbol(self, text):
        """Узнаем ID Коина"""
        with self.connection:
            result = self.cursor.execute("SELECT `id` FROM  `coinTables` WHERE `symbol` = ?", (text,)).fetchone()
            return(result[0])
            
            ###################################################################################################################################################
            """Закрываем соединение с БД"""
    def close(self):
        self.connection.close()