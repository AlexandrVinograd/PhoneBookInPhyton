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

    # Метод для добавления контакта в базу данных
    def add_contact(self, name, phone_number, email=None, birthday=None, address=None):
        self.cursor.execute('''INSERT INTO contacts (name, phone_number, email, birthday, address)
                                VALUES (?, ?, ?, ?, ?)''', (name, phone_number, email, birthday, address))
        self.conn.commit()

    # Метод для поиска контакта по имени
    def search_contact(self, name):
        self.cursor.execute('''SELECT * FROM contacts WHERE name LIKE ?''', ('%' + name + '%',))
        return self.cursor.fetchall()

    # Метод для удаления контакта по id
    def delete_contact(self, id):
        self.cursor.execute('''DELETE FROM contacts WHERE id=?''', (id,))
        self.conn.commit()

    # Метод для обновления контакта по id
    def update_contact(self, id, name=None, phone_number=None, email=None, birthday=None, address=None):
        update_query = '''UPDATE contacts SET '''
        update_values = []
        # Подготовка запроса на обновление и значений для обновления
        if name:
            update_query += '''name=?, '''
            update_values.append(name)
        if phone_number:
            update_query += '''phone_number=?, '''
            update_values.append(phone_number)
        if email:
            update_query += '''email=?, '''
            update_values.append(email)
        if birthday:
            update_query += '''birthday=?, '''
            update_values.append(birthday)
        if address:
            update_query += '''address=?, '''
            update_values.append(address)
        # Удаление последней запятой и добавление условия WHERE
        update_query = update_query.rstrip(', ')
        update_query += ''' WHERE id=?'''
        update_values.append(id)
        # Выполнение запроса на обновление
        self.cursor.execute(update_query, tuple(update_values))
        self.conn.commit()

    # Метод для просмотра всех контактов в базе данных
    def view_contacts(self):
        self.cursor.execute('''SELECT * FROM contacts''')
        return self.cursor.fetchall()

    # Метод для импорта контактов из файла
    def import_contacts(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(',')
                    # Разделение данных из строки и добавление контакта в базу данных
                    if len(data) >= 2:
                        name = data[0]
                        phone_number = data[1]
                        email = data[2] if len(data) >= 3 else None
                        birthday = data[3] if len(data) >= 4 else None
                        address = data[4] if len(data) >= 5 else None
                        self.add_contact(name, phone_number, email, birthday, address)
            print("Import successful.")
        else:
            print("File not found.")

    # Метод для закрытия соединения с базой данных
    def close_connection(self):
        self.cursor.close()
        self.conn.close()