"""
import datetime
import os
import random
import subprocess
import sys
import tkinter.filedialog as fd
import webbrowser
from os.path import join
from time import sleep
import psutil
import pyautogui
import pyperclip
import pytesseract
import pyttsx3
import speech_recognition as sr
from keyboard import press_and_release
import string
from ctypes import windll
import threading
import winapps

SayOpenPhrases = ['Уже открываю', 'Сейчас открою', 'Одну секунду', 'Сейчас все будет', 'Подожди немного, сейчас сделаю']
SayClosePhrases = ['Уже закрываю', 'Сейчас закрою', 'подождите немного, я выполняю закрытие', 'Сейчас все будет',
                   'Пожалуйста подождите', 'Так и быть закрою']
SayUnknownPhrases = ['Не известная команда', 'Такой команды не существует', 'Я вас не понимаю',
                     'Попробуй еще раз сказать']
SayByePhrases = ['Пока', 'До свидания', 'Надеюсь мы еще встретимся', 'Всего хорошего']

SayThanksPhrases = ['Не за что', 'Пожалуйста', 'Обращайтесь']

FileOpen = ["Counter-Strike Global Offensive.url", "steam.exe",
            "Discord.exe", "Telegram.exe", "GenshinImpact.exe"]

FileOpenPhrase = ["открой counter-strike", "открой стим",
                  "открой discord", "открой телеграм", "открой геншин"]

FileClose = ["csgo.exe", "explorer.exe", "notepad.exe", "win32calc.exe", "steam.exe",
             "Discord.exe", "Telegram.exe", "Taskmgr.exe", "GenshinImpact.exe", "opera.exe"]

FileClosePhrase = ["закрой counter-strike", "закрой проводник", "закрой блокнот", "закрой калькулятор", "закрой стим",
                   "закрой discord", "закрой телеграм", "закрой диспетчер", "закрой геншин", "закрой браузер"]

FileOpenSystem = ["explorer.exe", "notepad.exe", "win32calc.exe", "Taskmgr.exe"]

FileOpenSystemPhrase = ["открой проводник", "открой блокнот", "открой калькулятор", "открой диспетчер"]


def Speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def commandRu():
    OutFileName = open('../Files/Language.txt', 'w')
    OutFileName.write("Русский")
    OutFileName.close()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language="ru-RU").lower()
        except sr.UnknownValueError:
            Speak("Я вас не расслышал, повторите пожалуйста")
            text = commandRu()
        return text


def drag_window(self, event):
    self.root.geometry(f'+{event.x_root - dx}+{event.y_root - dy}')


def on_key_press(event):
    if event.keysym == 'Escape':
        root.destroy()


def start_drag(event):
    global dx, dy
    dx, dy = event.x, event.y


def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter + ":\\")
        bitmask >>= 1

    return drives


def open_file(drives, lookfor):
    flag = False
    for i in range(len(drives)):
        for root, dirs, files in os.walk(drives[i]):
            if lookfor in files:
                key = join(root, lookfor)
                os.startfile(key)
                flag = True
                break
        if flag:
            break


def close_file(lookfor):
    for process in (process for process in psutil.process_iter() if process.name() == lookfor):
        process.kill()


def delete_file(drives, lookfor):
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
        Speak("Удаление выполнено успешно!")
    else:
        Speak("Такого файла не существует!")


drives = get_drives()


def Open(text):
    for i in range(len(FileOpenPhrase)):
        if FileOpenPhrase[i] in text:
            open_file(drives, FileOpen[i])

    for i in range(len(FileOpenSystemPhrase)):
        if FileOpenSystemPhrase[i] in text:
            subprocess.Popen(FileOpenSystem[i])


def Close(text):
    for i in range(len(FileClosePhrase)):
        if FileClosePhrase[i] in text:
            close_file(FileClose[i])


def Greetings():
    Speak("Скажите мне как вас называть")
    text = commandRu()
    NameStatic = text
    YourName = "Вас зовут," + text + ",всё верно?"
    Speak(YourName)
    text = commandRu()
    if "да" in text:
        OutFileName = open('../Files/name.txt', 'w')
        OutFileName.write(NameStatic)
        OutFileName.close()
        NameStatic = "Привет," + NameStatic
        Speak(NameStatic)
    elif 'нет' in text:
        while 'нет' in text:
            Speak("Представьтесь еще раз")
            text = commandRu()
            Greetings()


def choose_file():
    filetypes = (("Текстовый файл", "*.txt"),
                 ("Изображение", "*.jpg *.gif *.png"),
                 ("Любой", "*"))
    filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                  filetypes=filetypes)
    if filename:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        Speak(pytesseract.image_to_string(filename, lang='rus'))


def scan_user_name():
    with open('../Files/name.txt') as f:
        name = f.readline()
    return name


def HelloUser():
    Name = scan_user_name()
    if len(Name) == 0:
        Speak("Имя пользователя не задано")
        Speak("Для начала скажите мне как Вас называть")
        SayName = commandRu()
        Greetings()
        Speak("Теперь можно и поговорить")
    else:
        Name = scan_user_name()
        t = threading.Thread(target=Animation())
        t.daemon = True
        t.start()
        Hello = "Привет," + Name
        Speak(Hello)
        Speak("Начнем работу")


# def WriteMessage():
# def SearchObject():
# Cordinate = pyautogui.locateOnScreen(r"C:\Users\Ghou72rus\Desktop\girlfrend.png")
# return Cordinate


# point = SearchObject()


def WriteMessage():
    def SearchObject():
        Cordinate = pyautogui.locateOnScreen(r"C:\Users\Ghou72rus\Desktop\girlfrend.png")
        return Cordinate

    point = SearchObject()

    def MoveMouse(Cordinate):
        pyautogui.click(Cordinate, duration=0.5)
        pyautogui.click(332, 960, duration=0.5)

    def paste(text):
        pyperclip.copy(text)
        press_and_release('ctrl + v')

    def typing(text, interval=0.0):
        buffer = pyperclip.paste()
        if not interval:
            paste(text)
        else:
            for char in text:
                paste(char)
                sleep(interval)
        pyperclip.copy(buffer)

    MoveMouse(point)
    Speak("Что написать?")
    Message = commandRu()
    typing(Message, 0.1)
    Speak("Отправить?")
    Answer = commandRu()
    while Answer != 'да':
        Answer = commandRu()

    if 'да' in Answer:
        point = pyautogui.locateOnScreen(r"C:\Users\Ghou72rus\Desktop\Enter.png")
        pyautogui.click(point, duration=0.5)
    else:
        pass


def operation_on_pc():
    counter = 0
    task = []
    temp = []
    for line in subprocess.check_output("tasklist").splitlines():
        if counter >= 3:
            task.append(line.split())
        else:
            counter += 1
    task = list(zip(*task))[0]
    for i in range(len(task)):
        temp.append(task[i].decode('Windows-1251'))
    temp = list(set(temp))
    for i in range(len(temp)):
        print(i, temp[i])
    return temp


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



def write_installed_app():
    apps = []
    for app in winapps.list_installed():
        apps.append(app.name)
    flag = False
    try:
        with open("../Files/installed_files.txt", "r+") as installed_files:
            for i in range(len(apps)):
                for j in range(len(apps)):
                    installed_app = installed_files.readline()
                    if installed_app.rstrip() == apps[i]:
                        flag = True
                        break
                    else:
                        flag = False
                if not flag:
                    installed_files.write(f"{apps[i]}\n")
    except:
        Speak("Некоторые файлы отсутствуют в системе")
        with open("../Files/installed_files.txt", "w") as installed_files:
            Speak("Сейчас я его создам")
        write_installed_app()


def check_file_on_pc(name_app_speak):
    with open("../Files/installed_files.txt", "r") as installed_file:
        while True:
            installed_app = installed_file.readline()
            if not installed_app:
                break
            if name_app_speak == installed_app.rstrip():
                return installed_app.rstrip()


def write_app_after_delete():
    os.remove("../Files/installed_files.txt")
    apps = []
    for app in winapps.list_installed():
        apps.append(app.name)
    with open("../Files/installed_files.txt", "w") as installed_files:
        for i in range(len(apps)):
            installed_files.write(f"{apps[i]}\n")


def delete_apps(delete_app_name):
    winapps.uninstall(delete_app_name, args=['/S'])
    write_app_after_delete()


def MakeSomething(text):
    replace_text = text
    if 'открой' in text:
        Speak(random.choices(SayOpenPhrases))
        Open(text)
    elif 'закрой' in text:
        Speak("Что хотите закрыть?")
        close_task = operation_on_pc()
        id_task = commandRu()
        try:
            close_file(close_task[id_task])
        except TypeError:
            Speak("Это не число!")
            id_task = commandRu()
        finally:
            try:
                close_file(close_task[id_task])
            except TypeError:
                print("Все равно не число!")
                commandRu()
    elif 'напиши сообщение' in text:
        WriteMessage()
    elif 'распознай текст' in text:
        choose_file()
    elif 'поменять имя' in text or "изменить имя" in text:
        Speak("Давайте поменяем")
        Greetings()
    elif 'пока' in text:
        Speak(random.choices(SayByePhrases))
        sys.exit()
    elif 'открой вк' in text or 'открой vk' in text or 'открой вконтакте' in text:
        Speak(random.choices(SayOpenPhrases))
        webbrowser.open_new_tab('https://vk.com')
    elif 'привет' in text or 'здарова' in text:
        Speak("Привет)")
    elif 'стоп' in text:
        Speak("хорошо")
        exit()
    elif 'спасибо' in text or 'благодарю' in text:
        Speak(random.choices(SayThanksPhrases))
    elif replace_text.count('найди') == 1:
        Speak("Уже ищу")
        replace_text = replace_text.replace('найди', '')
        webbrowser.open_new_tab('https://yandex.ru/search/?clid=2358536&text=' + replace_text)
    elif "выключи компьютер" in text:
        Speak("Сейчас выключу, всего хорошего!")
        os.system("shutdown /s /t 1")
    elif 'время' in text or 'cкажи время' in text or 'сколько сейчас времени' in text or 'сколько время' in text:
        Speak("Сейчас")
        date_time = datetime.datetime.now().time()
        date_time = date_time.strftime('%H:%M')
        Speak(date_time)
        Speak("по московскому времени")
    elif 'ютуб' in text or 'youtube' in text or 'открой youtube' in text:
        Speak("Открываю youtube")
        webbrowser.open_new_tab('https://www.youtube.com')
    elif 'погода' in text or 'покажи погоду' in text or 'погода сейчас' in text:
        Speak("Сейчас покажу")
        webbrowser.open_new_tab('https://yandex.ru/pogoda')
    elif 'запиши в блокнот' in text:
        import Search
        Search.Start()
    elif 'удали' in text:
        Speak("Назовите имя файла и его расширение для удаления")
        name_delete_file = commandRu()
        delete_file(drives, name_delete_file)
    elif 'удали приложение' in text:
        Speak("Чтобы удалить приложение?")
        name_app_speak = commandRu()
        delete_apps(check_file_on_pc(name_app_speak))
    elif "включи музыку" in text:
        Speak("Что хотите послушать?")
        from Script import List
        List.main("../Files/music.json")
        for t in threading.enumerate():
            print(f'Thread Name: {t.name}')
    else:
        Speak(random.choices(SayUnknownPhrases))
        MakeSomething(commandRu())


def main():
    write_installed_app()
    HelloUser()
    while True:
        MakeSomething(commandRu())


if __name__ == "__main__":
    from Script.animation import main as Animation
    main()"""



