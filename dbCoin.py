import sqlite3
from dateNow import *

class SQLighterCoins:

    def __init__(self, database):
        print(database)
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
        
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