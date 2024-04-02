import sqlite3
import os

# Класс для работы с телефонным справочником
class PhoneBook:
    def __init__(self, db_name):
        # Подключение к базе данных
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Создание таблицы контактов, если она не существует
        self.create_table()

    def create_table(self):
        # Создание таблицы contacts с полями id, name, phone_number, email, birthday, address
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                phone_number TEXT NOT NULL,
                                email TEXT,
                                birthday TEXT,
                                address TEXT
                                )''')
        self.conn.commit()
