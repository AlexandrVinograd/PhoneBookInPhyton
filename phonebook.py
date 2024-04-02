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


# Функция для отображения меню и обработки выбора пользователя
def menu():
    print("Phonebook Menu:")
    print("1. Add contact")
    print("2. Search contact")
    print("3. Delete contact")
    print("4. Update contact")
    print("5. View all contacts")
    print("6. Import contacts")
    print("7. Exit")
    choice = input("Enter your choice: ")
    return choice


# Основная функция программы
def main():
    # Создание объекта телефонного справочника
    phonebook = PhoneBook('phonebook.db')
    while True:
        # Отображение меню и обработка выбора пользователя
        choice = menu()
        if choice == '1':
            # Запрос данных для добавления нового контакта
            name = input("Enter name: ")
            phone_number = input("Enter phone number: ")
            email = input("Enter email: ")
            birthday = input("Enter birthday: ")
            address = input("Enter address: ")
            # Добавление нового контакта
            phonebook.add_contact(name, phone_number, email, birthday, address)
            print("Contact added successfully.")
        elif choice == '2':
            # Поиск контакта по имени
            name = input("Enter name to search: ")
            result = phonebook.search_contact(name)
            if result:
                for row in result:
                    print(row)
            else:
                print("Contact not found.")
        elif choice == '3':
            # Удаление контакта по id
            id = input("Enter ID of contact to delete: ")
            phonebook.delete_contact(id)
            print("Contact deleted successfully.")
        elif choice == '4':
            # Обновление контакта по id
            id = input("Enter ID of contact to update: ")
            name = input("Enter new name: ")
            phone_number = input("Enter new phone number: ")
            email = input("Enter new email: ")
            birthday = input("Enter new birthday: ")
            address = input("Enter new address: ")
            phonebook.update_contact(id, name, phone_number, email, birthday, address)
            print("Contact updated successfully.")
        elif choice == '5':
            # Просмотр всех контактов
            contacts = phonebook.view_contacts()
            for contact in contacts:
                print(contact)
        elif choice == '6':
            # Импорт контактов из файла
            filename = input("Enter filename to import: ")
            phonebook.import_contacts(filename)
        elif choice == '7':
            # Закрытие соединения с базой данных и выход из программы
            phonebook.close_connection()
            break
        else:
            print("Invalid choice. Please try again.")

# Запуск основной функции программы, если файл запускается напрямую
if __name__ == "__main__":
    main()