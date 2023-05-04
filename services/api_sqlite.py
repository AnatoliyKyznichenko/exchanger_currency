import sqlite3
import os


def dict_factory(cursor, row): # cursor = database.cursor object, row: tuple
    save_dict = dict()
    for index, column in enumerate(cursor.description):
        save_dict[column[0]] = row[index]
    return save_dict


class Admin:
    def __init__(self):
        self.database = sqlite3.connect(os.path.join('data', 'database.db'))
        self.cursor = self.database.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS buy(
                            USD REAL DEFAULT 0,
                            EUR REAL DEFAULT 0,
                            PLN REAL DEFAULT 0,
                            GBP REAL DEFAULT 0,
                            CHF REAL DEFAULT 0,
                            CNY REAL DEFAULT 0,
                            CAD REAL DEFAULT 0
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sale(
                                    USD REAL DEFAULT 0,
                                    EUR REAL DEFAULT 0,
                                    PLN REAL DEFAULT 0,
                                    GBP REAL DEFAULT 0,
                                    CHF REAL DEFAULT 0,
                                    CNY REAL DEFAULT 0,
                                    CAD REAL DEFAULT 0
                )''')
        self.database.commit()

        #ЕСЛИ ХОТЯ БЫ В ОДНОЙ КОЛОНКИ НЕТ ДАННЫХ ТО МЫ ДОБАВЛЯЕМ ТУДА НУЛИ
        try:
            self.get_all_currency_dict('sale')['USD']
        except TypeError:
            self.cursor.execute('INSERT INTO sale VALUES (0,0,0,0,0,0,0)')
            self.cursor.execute('INSERT INTO buy VALUES (0,0,0,0,0,0,0)')
            self.database.commit()

    def get_all_currency(self, method):
        return self.cursor.execute(f'SELECT * FROM {method}').fetchall()[0] #кортеж из всех курсов валют

    def get_all_currency_dict(self, method):
        self.cursor.row_factory = dict_factory
        cur = self.cursor.execute(f'SELECT * FROM {method}').fetchall()
        return cur[0] if cur else None

    def update_currency(self, coin, method, amount):
        self.cursor.execute(f"UPDATE {method} SET '{coin}'={amount}")
        self.database.commit()
