import ctypes
import datetime
import getpass
import os
import pathlib
import random
import socket
import string
import subprocess
import threading
import time
import tkinter as tk
import webbrowser
from ctypes import windll
from itertools import cycle
from os.path import join
from tkinter import filedialog
import keyboard
import psutil
import pyautogui
import pygame as pygame
import pyperclip
import pytesseract
import pyttsx3
import requests
import speech_recognition as sr
import winapps
from bs4 import BeautifulSoup
from googletrans import Translator
import screen_brightness_control as sbc

from Script import extractor
from Script.sound import Sound


class Waiter(threading.Thread):
    def __init__(self):
        super().__init__()
        self.flag = False
        self.jora = Jora()

    def run(self):
        try:
            socket.create_connection(("www.google.com", 80))
            self.flag = True
        except:
            self.flag = False
        while True:
            if not self.flag:
                while True:
                    try:
                        socket.create_connection(("www.google.com", 80))
                        self.flag = True
                        # self.jora.Speak("Подключение к интернету установлено")
                        time.sleep(60)
                        break
                    except:
                        self.flag = False
                        time.sleep(60)
                        break
            else:
                while True:
                    try:
                        socket.create_connection(("www.google.com", 80))
                        time.sleep(60)
                        break
                    except:
                        self.flag = False
                        # self.jora.Speak("Подключение к интернету отсутствует")
                        time.sleep(60)
                        break


class Jora(object):
    def __init__(self):
        self.Sound = Sound()
        self.current_volume = 50
        self.music_first = True
        self.user = os.environ['USERNAME']
        self.Extractor = extractor.NumberExtractor()
        self.Start_Flag = True
        self.drives = self.get_drives()
        self.shake = False
        self.current_brightness = sbc.get_brightness()

        self.SayOpenPhrases = ['Уже открываю', 'Сейчас открою', 'Одну секунду', 'Сейчас все будет',
                               'Подожди немного, сейчас сделаю']
        self.SayClosePhrases = ['Уже закрываю', 'Сейчас закрою', 'подождите немного, я выполняю закрытие',
                                'Сейчас все будет',
                                'Пожалуйста подождите', 'Так и быть закрою']
        self.SayUnknownPhrases = ['Не известная команда', 'Такой команды не существует', 'Я вас не понимаю',
                                  'Попробуй еще раз сказать']
        self.SayByePhrases = ['Пока', 'До свидания', 'Надеюсь мы еще встретимся', 'Всего хорошего']

        self.SayThanksPhrases = ['Не за что', 'Пожалуйста', 'Обращайтесь']

        self.FileOpen = ["Counter-Strike Global Offensive.url", "steam.exe",
                         "Discord.exe", "Telegram.exe", "GenshinImpact.exe"]

        self.FileOpenPhrase = ["открой counter-strike", "открой стим",
                               "открой discord", "открой telegram", "открой геншин"]

        self.FileClose = ["csgo.exe", "explorer.exe", "notepad.exe", "win32calc.exe", "steam.exe",
                          "Discord.exe", "Telegram.exe", "Taskmgr.exe", "GenshinImpact.exe", "opera.exe", "python.exe"]

        self.FileClosePhrase = ["закрой counter-strike", "закрой проводник", "закрой блокнот", "закрой калькулятор",
                                "закрой стим",
                                "закрой discord", "закрой telegram", "закрой диспетчер", "закрой геншин",
                                "закрой браузер", "python.exe"]

        self.FileOpenSystem = ["explorer.exe", "notepad.exe", "win32calc.exe", "Taskmgr.exe", "mspaint.exe"]

        self.FileOpenSystemPhrase = ["открой проводник", "открой блокнот", "открой калькулятор", "открой диспетчер",
                                     "открой paint"]

    def Speak(self, text):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == "Artemiy":
                self.engine.setProperty('voice', voice.id)
                self.engine.setProperty('rate', 160)
        self.engine.say(text)
        self.engine.runAndWait()

    def add_to_startup(self):
        USER_NAME = getpass.getuser()
        file_path = self.find_file("Жора трей\Жора трей.exe.lnk")
        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
        with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
            bat_file.write(r'start "" %s' % file_path)

    def check_micro(self):
        try:
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    self.Start_Flag = True
            except OSError:
                self.Speak("У вас нет микрофона или доступ к нему ограничен")
        except AttributeError:
            self.Start_Flag = False
            self.Speak("У вас нет микрофона или доступ к нему ограничен")
            time.sleep(60)
            self.check_micro()

    def commandRu(self):
        OutFileName = open('Files/Language.txt', 'w')
        OutFileName.write("Русский")
        OutFileName.close()
        try:
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    self.Start_Flag = True
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio_text = r.listen(source)
                    try:
                        text = r.recognize_google(audio_text, language="ru-RU").lower()
                        return text
                    except sr.UnknownValueError:
                        self.commandRu()
            except OSError:
                self.check_micro()
        except AttributeError:
            self.Start_Flag = False
            self.Speak("У вас не хватает библиотек")

    def find_file(self, name_file):
        cur_dir = os.getcwd().split(":")
        cur_dir[0] += ":\\"
        drivers = self.get_drives()
        drivers.remove(cur_dir[0])
        for root, dirs, files in os.walk(cur_dir[0]):
            if name_file in files:
                key = join(root, name_file)
                return key
        for i in range(len(drivers)):
            for root, dirs, files in os.walk(drivers[i]):
                if name_file in files:
                    key = join(root, name_file)
                    return key

    def get_drives(self):
        self.drives = []
        self.bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if self.bitmask & 1:
                self.drives.append(letter + ":\\")
            self.bitmask >>= 1

        return self.drives

    def open_file(self, drives, lookfor):
        self.flag = False
        for i in range(len(drives)):
            for root, dirs, files in os.walk(drives[i]):
                if lookfor in files:
                    key = join(root, lookfor)
                    os.startfile(key)
                    self.flag = True
                    break
            if self.flag:
                break

    def close_file(self, lookfor):
        for process in (process for process in psutil.process_iter() if process.name() == lookfor):
            try:
                process.kill()
            except psutil.AccessDenied:
                self.Speak("отказано в доступе!")
                break
            except psutil.NoSuchProcess:
                pass

    def delete_file(self, drives, lookfor):
        flag = False
        Delete_flag = False
        for i in range(len(drives)):
            for root, dirs, files in os.walk(drives[i]):
                if lookfor in files:
                    key = join(root, lookfor)
                    os.remove(key)
                    Delete_flag = True
                    flag = True
                    break
            if flag:
                break
        if Delete_flag:
            self.Speak("Удаление выполнено успешно!")
        else:
            self.Speak("Такого файла не существует!")

    def Open(self, text):
        for i in range(len(self.FileOpenPhrase)):
            if self.FileOpenPhrase[i] in text:
                self.open_file(self.drives, self.FileOpen[i])

        for i in range(len(self.FileOpenSystemPhrase)):
            if self.FileOpenSystemPhrase[i] in text:
                try:
                    subprocess.Popen(self.FileOpenSystem[i])
                except FileNotFoundError:
                    self.start_and_end_animation()
                    self.Speak("Указаной вами программы нет на вашем компьютере")

    def Close(self, text):
        for i in range(len(self.FileClosePhrase)):
            if self.FileClosePhrase[i] in text:
                self.close_file(self.FileClose[i])

    def Greetings(self):
        self.Speak("Скажите мне как вас называть")
        text = self.commandRu()
        NameStatic = text
        YourName = "Вас зовут," + text + ",всё верно?"
        self.Speak(YourName)
        self.Speak("Скажите да чтобы подтвердить или скажите нет чтобы задать имя занаво")
        while True:
            text = self.commandRu()
            if "да" in text:
                OutFileName = open('Files/name.txt', 'w')
                OutFileName.write(NameStatic)
                OutFileName.close()
                NameStatic = "Привет," + NameStatic
                self.Speak(NameStatic)
                break
            elif 'нет' in text:
                self.Speak("Представьтесь еще раз")

    def selectCustomerFileTK(self):
        root = tk.Tk()
        root.wm_attributes('-topmost', 1)
        root.withdraw()
        filename = filedialog.askopenfilename()
        return filename

    def choose_file(self):
        print(1)
        image = pyautogui.screenshot()
        image.crop((300, 300, 800, 800)).save("temp/1.png")
        try:
            tessdata_dir_config = r'--tessdata-dir r"C:\Program Files (x86)\Tesseract-OCR\tessdata"'
            pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
            self.Speak(pytesseract.image_to_string('temp/1.png', lang='rus', config=tessdata_dir_config))
        except pytesseract.pytesseract.TesseractNotFoundError:
            self.Speak("у вас не установлена специальная библиотека для распознания текста")

    def speak_document(self):
        os.startfile('Чтение документа\Чтение документа.exe')

    def scan_user_name(self):
        with open('Files/name.txt') as f:
            self.name = f.readline()
        return self.name

    def HelloUser(self):
        Name = self.scan_user_name()
        if len(Name) == 0:
            self.Speak("Имя пользователя не задано")
            self.Greetings()
            self.start_and_end_animation()
            self.Speak("Теперь можно и поговорить")
        else:
            Name = self.scan_user_name()
            Hello = "Привет," + Name
            self.Speak(Hello)
            time.sleep(0.05)
            self.Speak("Начнем работу")

    def operation_on_pc(self):
        self.counter = 0
        self.task = []
        self.temp = []
        for line in subprocess.check_output("tasklist").splitlines():
            if self.counter >= 3:
                self.task.append(line.split())
            else:
                self.counter += 1
        self.task = list(zip(*self.task))[0]
        for i in range(len(self.task)):
            self.temp.append(self.task[i].decode('Windows-1251'))
        self.temp = list(set(self.temp))
        with open("Files/tasklist.txt", 'w') as file:
            for i in range(len(self.temp)):
                file.write(self.temp[i] + '\n')

    """"
    def on_press(x, y, button, pressed):
        global first_x, first_y, second_x, second_y
        if pressed:
            print(F"Pressed at {x, y}")
            first_x, first_y = x, y
        else:
            second_x, second_y = x, y
            print(f"Released at {x, y}")
    
        if not pressed:
            # Stop listener
            return False
    
    sleep(3)
    with Listener(on_click=on_press) as listener:
        listener.join()
    minim_x = min(first_x, second_x)
    maxim_x = max(first_x, second_x)
    
    minim_y = min(first_y, second_y)
    maxim_y = max(first_y, second_y)
    
    im = (ImageGrab.grab(bbox=(minim_x, minim_y, maxim_x, maxim_y)))
    im.show()
    """

    def write_installed_app(self):
        self.apps = []
        for app in winapps.list_installed():
            self.apps.append(app.name)
        flag = False
        try:
            with open("Files/installed_files.txt", "r+") as installed_files:
                for i in range(len(self.apps)):
                    for j in range(len(self.apps)):
                        installed_app = installed_files.readline()
                        if installed_app.rstrip() == self.apps[i]:
                            flag = True
                            break
                        else:
                            flag = False
                    if not flag:
                        installed_files.write(f"{self.apps[i]}\n")
        except:
            self.Speak("Некоторые файлы отсутствуют в системе")
            with open("Files/installed_files.txt", "w") as installed_files:
                self.Speak("Сейчас я его создам")
            self.write_installed_app()

    def check_file_on_pc(self, name_app_speak):
        with open("Files/installed_files.txt", "r") as installed_file:
            while True:
                self.installed_app = installed_file.readline()
                if not self.installed_app:
                    break
                if name_app_speak == self.installed_app.rstrip():
                    return self.installed_app.rstrip()

    def start_and_end_animation(self):
        try:
            os.startfile(r"Анимация\анимация.exe")
        except FileNotFoundError:
            self.Speak("Нет файла с анимацией")

    def write_app_after_delete(self):
        os.remove("Files/installed_files.txt")
        self.apps = []
        for app in winapps.list_installed():
            self.apps.append(app.name)
        with open("Files/installed_files.txt", "w") as installed_files:
            for i in range(len(self.apps)):
                installed_files.write(f"{self.apps[i]}\n")

    def delete_apps(self, delete_app_name):
        winapps.uninstall(delete_app_name, args=['/S'])
        self.write_app_after_delete()

    def change_word_to_number(self, text):
        if " точка " in text:
            text = text.replace(" точка ", ".")
        if " двоеточие " in text:
            text = text.replace(" двоеточие ", ":")
        text = self.Extractor.replace_groups(text)
        return text

    def set_start_volume(self):
        Sound.volume_set(self.current_volume)

    def switch_window(self):
        keyboard.send("alt + tab")
        keyboard.press("alt")
        while True:
            text = self.commandRu()
            if "вперёд" in text:
                self.forward_video()
            elif "назад" in text:
                self.backward_video()
            elif "открой" in text:
                keyboard.release("alt")
                break

    def todo_start(self):
        os.spawnv(os.P_NOWAIT, r"venv\Scripts\python.exe",
                  ("python", "Script/todo"
                             ".py"))

    def end_page(self):
        keyboard.send("page down")

    def start_page(self):
        keyboard.send("page up")

    def fullcreen_video(self):
        keyboard.send("f")

    def forward_video(self):
        keyboard.send("right")

    def backward_video(self):
        keyboard.send("left")

    def math_replace(self, text):
        math_text = self.change_word_to_number(text)
        if "плюс" in math_text or "plus" in math_text:
            math_text = math_text.replace("плюс", "+")
            math_text = math_text.replace("plus", "+")
        if "минус" in math_text:
            math_text = math_text.replace("минус", "-")
        if "х" in math_text:
            math_text = math_text.replace("х", "*")
        if "разделить" in math_text or "делить" in math_text:
            math_text = math_text.replace("разделить ", "/")
            math_text = math_text.replace("делить ", "/")
        if "точка" in math_text or "запятая" in math_text:
            math_text = math_text.replace("точка", ".")
            math_text = math_text.replace("запятая", ".")
        if "на" in text:
            math_text = math_text.replace("на", "")
        if "корень из" in math_text:
            math_text = math_text.replace("корень из ", " (")
            delete_symbols = "йцукенгшщзхъфывапролджэячсмитьбю"
            temp = list(math_text)
            for i in range(len(math_text)):
                for j in range(len(delete_symbols)):
                    if temp[i] == delete_symbols[j]:
                        temp[i] = ''
                        math_text = "".join(temp)
            math_text = math_text.split()
            for i in range(len(math_text)):
                if math_text[i] == '*' or math_text[i] == '-' or math_text[i] == '/' or math_text[i] == '+':
                    buf = math_text[i - 1] + "**0.5)"
                    math_text[i - 1] = math_text[i - 1].replace(math_text[i - 1], buf)
                elif i == len(math_text) - 1 and '(' in math_text[i]:
                    buf = math_text[i] + "**0.5)"
                    math_text[i] = math_text[i].replace(math_text[i], buf)
            math_text = ''.join(map(str, math_text))
        try:
            self.Speak(eval(math_text))
        except:
            self.Speak("Неправильное математическое выражение")

    class Save:
        @staticmethod
        def paste(text):
            pyperclip.copy(text)
            keyboard.press_and_release('ctrl + v')

        def type(self, text, interval=0.2):
            buffer = pyperclip.paste()
            if not interval:
                self.paste(text)
            else:
                for char in text:
                    self.paste(char)
                    time.sleep(interval)
            pyperclip.copy(buffer)

        def write_message(self):
            while True:
                text = Jora.commandRu(Jora())
                if text != "отправь":
                    self.type(text + " ", 0.2)
                    time.sleep(1)
                else:
                    break

        def SaveFile(self):
            keyboard.press_and_release("enter")

        def Start(self):
            self.write_message()
            self.SaveFile()

    def MakeSomething(self, text):
        replace_text = text
        try:
            if 'открой' in text:
                self.Speak(random.choices(self.SayOpenPhrases))
                self.Open(text)

            elif "покажи последний скриншот" == text:
                p = pathlib.Path(r"Screenshots\\")
                for x in p.rglob("*"):
                    os.startfile(x)
                    break
            elif "переключи окно" == text:
                self.switch_window()

            elif 'закрой' in text:
                self.Close(text)

            elif 'распознай текст' in text:
                self.choose_file()

            elif 'поменять имя' == text or "изменить имя" == text:
                self.Speak("Давайте поменяем")
                self.Greetings()

            elif 'открой вк' == text or 'открой vk' == text or 'открой вконтакте' == text:
                self.Speak(random.choices(self.SayOpenPhrases))
                webbrowser.open_new_tab('https://vk.com')

            elif 'привет' == text or 'здарова' == text:
                self.Speak("Привет)")

            elif 'пока жора' in text:
                self.Speak(random.choices(self.SayByePhrases))
                os.startfile('Жора трей\Жора трей.exe')
                time.sleep(10)
                self.close_file('Анимация.exe')
                self.close_file('Радио.exe')
                self.close_file('Чтение документа.exe')
                self.close_file('Музыка.exe')
                self.close_file('Запись.exe')
                self.close_file('Камера.exe')
                self.close_file('Список музыки.exe')
                self.close_file('Список радио.exe')
                self.close_file('Загрузка видео.exe')
                self.close_file('one_service_run.exe')
                self.close_file("Жора.exe")

            elif 'спасибо' == text or 'благодарю' == text:
                self.Speak(random.choices(self.SayThanksPhrases))

            elif replace_text.count('найди') == 1:
                self.Speak("Уже ищу")
                replace_text = replace_text.replace('найди', '')
                webbrowser.open_new_tab('https://yandex.ru/search/?clid=2358536&text=' + replace_text)

            elif "выключи компьютер" == text:
                self.Speak("Сейчас выключу, всего хорошего!")
                os.system("shutdown /s /t 1")

            elif 'время' == text or 'cкажи время' == text or 'сколько сейчас времени' == text or 'сколько время' == text:
                date_time = datetime.datetime.now().time()
                date_time = date_time.strftime('%H:%M')
                self.Speak(date_time + "по московскому времени")

            elif 'ютуб' in text or 'youtube' in text or 'открой youtube' in text:
                self.Speak("Открываю youtube")
                webbrowser.open_new_tab('https://www.youtube.com')

            elif 'погода' == text or 'посмотри погоду' == text or 'погода сейчас' == text:
                self.Speak("Сейчас покажу")
                webbrowser.open_new_tab('https://yandex.ru/pogoda')

            elif 'запиши в блокнот' == text:
                try:
                    os.startfile("Запись\Запись.exe")
                except FileNotFoundError:
                    self.Speak("Модуля записи не был найден. Невозможно записать")
            elif 'удали' == text:
                self.Speak("Назовите имя файла и его расширение для удаления")
                name_delete_file = self.commandRu()
                self.delete_file(self.drives, name_delete_file)

            elif 'удали приложение' == text:
                self.Speak("Чтобы удалить приложение?")
                self.delete_apps(self.check_file_on_pc(self.commandRu()))

            elif "запусти player" in text:
                self.Speak("Сейчас все сделаю")
                try:
                    os.startfile("Музыка\Музыка.exe")
                except FileNotFoundError:
                    self.Speak("Модуль музыки не был найден. Невозможно запустить плеер")
            elif "запусти камеру" == text:
                self.Speak("Скажите айпи и порт вашей камеры")
                os.startfile("Камера\Камера.exe")

            elif "выключи камеру" == text:
                self.close_file("Камера.exe")

            elif "потише" == text:
                self.current_volume -= 5
                self.Sound.volume_set(self.current_volume)

            elif "погромче" == text:
                self.current_volume += 5
                self.Sound.volume_set(self.current_volume)

            elif "выключи звук" == text:
                self.Sound.volume_set(0)

            elif "вперёд" == text:
                self.forward_video()

            elif "назад" == text:
                self.backward_video()

            elif "вниз" == text:
                self.end_page()

            elif "вверх" == text:
                self.start_page()

            elif "разверни" == text:
                self.fullcreen_video()

            elif "включи звук" == text:
                self.Sound.volume_set(self.current_volume)

            elif "напомни мне" == text:
                pass
            elif 'поставь в автозапуск' == text:
                self.add_to_startup()
                self.Speak("Жора был успешно добавлен в автозагрузку")
            elif "сделай скриншот" in text:
                image = pyautogui.screenshot()
                path_and_name = r"Screenshots\screenshot_" + str(
                    datetime.datetime.now().replace(microsecond=0)) + ".png"
                path_and_name = path_and_name.replace(" ", "_").replace("-", "_").replace(":", "_")
                image.save(path_and_name)
            elif "установи громкость на" in text:
                text = text.replace("установи громкость на", "")
                self.current_volume = self.change_word_to_number(text)
                num = [int(x) for x in self.current_volume.split() if x.isdigit()]
                if num[0] < 0 or num[0] > 100:
                    self.Speak("нельзя установить такую громкость")
                else:
                    self.current_volume = num[0]
                    self.Sound.volume_set(self.current_volume)
            elif "запусти радио" == text or "включи радио" == text:
                try:
                    os.startfile("Радио\Радио.exe")
                except FileNotFoundError:
                    self.Speak("Модуль с радио не был найден. Невозможно запустить радио")
            elif 'выключи радио' == text:
                self.close_file('Радио.exe')
            elif "прочитай документ" in text:
                self.speak_document()
            elif "перестань читать" in text:
                self.close_file("Чтение документа.exe")
            elif "сколько будет" in text:
                text = text.replace("сколько будет", '')
                self.math_replace(text)
            elif "пиши" in text:
                self.Speak("Сейчас буду писать, диктуйте!")
                save = Jora.Save()
                save.Start()
                del save
            elif 'давай сыграем' in text or 'давай поиграем' in text:
                self.game()
            elif 'расскажи анекдот' in text:
                self.Speak(self.generate_joke())
            elif 'какой сегодня день' in text:
                self.Speak("сегодня " + self.day_today())
            elif 'скачай видео' in text:
                os.startfile("Загрузка видео\Загрузка видео.exe")
            elif 'переведи на русский' in text:
                text = text.replace('переведи на русский', '')
                self.translate_text_ru(text)
            elif 'переведи на английский' in text:
                text = text.replace('переведи на английский', '')
                self.translate_text_en(text)
            elif "выключи монитор" in text:
                self.screen_off()
            elif "включи монитор" in text:
                self.screen_on()
            elif "ночной режим" in text:
                self.set_brightness_dark()
                self.current_brightness[0] = 10
            elif "светлый режим" in text:
                self.set_brightness_white()
            elif "поярче" in text:
                self.set_brightness_up()
                self.current_brightness[0] += 5
            elif "потемнее" in text:
                self.set_brightness_low()
                self.current_brightness[0] -= 5
            elif "установи яркость на" in text:
                text = text.replace("установи яркость на", "")
                self.current_brightness = self.change_word_to_number(text)
                self.set_brightness_user(self.current_brightness)
            elif "выйди из системы" in text:
                self.exit_system()
            elif "спящий режим" in text:
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

            else:
                if self.Start_Flag:
                    self.MakeSomething(self.commandRu())
                else:
                    pass
        except TypeError:
            pass

    def Parallel(self, func):
        self.th = threading.Thread(target=func())
        self.th.daemon = True
        self.th.start()

    def Start(self):
        os.startfile(r"one_service_run\one_service_run.exe")
        self.set_start_volume()
        self.check_micro()
        if self.Start_Flag:
            self.start_and_end_animation()
            self.write_installed_app()
            self.HelloUser()
            self.todo_start()
            while True:
                self.MakeSomething(self.commandRu())
        else:
            self.check_micro()

    def game(self):
        self.Speak('Вы начинаете')

        def normalize_city_name(name):
            return name.strip().lower().replace('ё', 'е')

        cache = set()
        cities = {normalize_city_name(x) for x in open("Files/cities.txt", "r").readlines() if x.strip()}
        check_list = []

        with open("Files/cities.txt", "r") as f:
            cities = {normalize_city_name(x) for x in f.readlines() if x.strip()}

        def user_point(char):
            user_say = self.commandRu()  # 1
            if 'стоп' in user_say or 'хватит играть' in user_say:
                self.Speak("Больше не играем")
                return 0
            else:
                city = normalize_city_name(user_say)  # 2
                kw = {"char": char, "cache": cache, "cities": cities}  # 3
                if not all(x(city, **kw) for x in check_list):  # 4
                    return user_point(char)  # 5
                return city

        def check_point(fun):
            check_list.append(fun)
            return fun

        @check_point
        def is_city_startswith_char(city, char, **kwargs):
            if char is None or city.startswith(char):
                return True
            else:
                self.Speak(f'Город должен начинаться с буквы {char.capitalize()}')
                return False

        @check_point
        def is_non_cached(city, cache, **kwargs):
            if city not in cache:
                return True
            else:
                self.Speak("Этот город уже был назван")
                return False

        @check_point
        def is_available(city, cities, **kwargs):
            if city in cities:
                return True
            else:
                self.Speak("Я такого города не знаю")
                return False

        def move_to_cache(city, cities, cache):
            cities.remove(city)
            cache.add(city)

        def get_next_char(city):
            wrong_char = ("Ъ", "ь", "ы", "й")
            for char in city[::-1]:
                if char in wrong_char:
                    continue
                else:
                    break
            else:
                raise RuntimeError
            return char

        def ai_point(char):
            for city in cities:
                if city.startswith(char):
                    break
            else:
                raise SystemExit(self.Speak("Вы победили!"))
            self.Speak(city)
            return city

        def start_game():
            char = None
            for point in cycle((user_point, ai_point)):
                if point(char) == 0:
                    break
                else:
                    next_city = point(char)
                    move_to_cache(next_city, cities, cache)
                    char = get_next_char(next_city)

        start_game()

    def generate_joke(self):
        url = "https://randstuff.ru/joke"
        try:
            r = requests.get(url, verify=False)
            soup = BeautifulSoup(r.text, 'lxml', )
            table = soup.find('table', attrs={"class:", "text"})
            joke = table.text
            return joke
        except:
            self.Speak("Не удалось сгенерировать шутку")

    def day_today(self):
        day = datetime.datetime.now()
        day = day.weekday()
        if day == 0:
            return "понедельник"
        elif day == 1:
            return "вторник"
        elif day == 2:
            return "среда"
        elif day == 3:
            return "четверг"
        elif day == 4:
            return "пятница"
        elif day == 5:
            return "суббота"
        elif day == 6:
            return "воскресенье"

    def translate_text_ru(self, text):
        t = Translator()
        translate_text = t.translate(text, dest='ru')
        self.Speak(translate_text.text)

    def translate_text_en(self, text):
        t = Translator()
        translate_text = t.translate(text, dest='en')
        print(translate_text.text)
        self.Speak(translate_text.text)

    def screen_off(self):
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)

    def screen_on(self):
        ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)

    def set_brightness_dark(self):
        sbc.set_brightness(10)

    def set_brightness_white(self):
        sbc.set_brightness(100)

    def set_brightness_low(self):
        sbc.set_brightness((self.current_brightness[0] - 5))

    def set_brightness_up(self):
        sbc.set_brightness((self.current_brightness[0] + 5))

    def set_brightness_user(self, text):
        sbc.set_brightness(text)

    def exit_system(self):
        ctypes.windll.user32.ExitWindowsEx(0, 1)

    def resize_screen(self):
        pygame.init()
        pygame.display.set_mode()

    def enable_wifi(self):
        os.system('chcp 65001')
        wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
        data = wifi.decode(encoding='unicode_escape', errors='replace')
        if "There is no wireless interface on the system." in data:
            self.Speak("У вас нет вайфай модуля")
        else:
            os.system("netsh interface set interface 'Wifi' enabled")

    def disable_wifi(self):
        os.system('chcp 65001')
        wifi = subprocess.check_output(['netsh', 'WLAN', 'show', 'interfaces'])
        data = wifi.decode(encoding='unicode_escape', errors='replace')
        if "There is no wireless interface on the system." in data:
            self.Speak("У вас нет вайфай модуля")
        else:
            os.system("netsh interface set interface 'Wifi' disabled")


if __name__ == '__main__':
    waiter = Waiter()
    waiter.start()
    time.sleep(5)
    jora = Jora()
    if waiter.flag:
        jora.Speak("Проверка подключения к интернету прошла успешна")
        jora.Start()

    else:
        jora.Speak("Проверка подключения к интернету не была пройдена, работа Жоры невозможно")
        jora.close_file("Жора.exe")
