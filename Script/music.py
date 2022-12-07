import json
import os
import random
import string
import threading
import time
from ctypes import windll
from os.path import join
import psutil
import speech_recognition as sr
import pyttsx3
from playsound import playsound
from mutagen.mp3 import MP3
from extractor import NumberExtractor


class Waiter(threading.Thread):
    def __init__(self):
        super().__init__()
        self.lenght_music_buf = 0
        self.next_music = 0
        self.lenght_music = None

    def run(self, music_name):
        self.lenght_music, self.next_music = Music.get_id_and_lenght_music(Music(), music_name)
        print(self.lenght_music)
        while True:
            time.sleep(1)
            self.lenght_music_buf += 1
            if self.lenght_music_buf == self.lenght_music:
                print(2)
                self.next_music += 1
                self.lenght_music_buf = 0
                Music.next_music_start(Music(), self.next_music, shake=Music.get_shake(Music()),
                                       first=Music.get_first(Music()))
                self.run(self.next_music)


class Music(object):

    def __init__(self):
        self.first = True
        self.shake = False
        self.music_shake = []
        self.musik_random = self.shake_music()
        self.next_music = 0
        self.lenght_music = None
        self.music = None
        self.lenght_music_buf = 0
        self.drives = []
        self.max_music_id = 0
        self.file = "../Files/music.json"

    def start_and_end_animation(self):
        os.startfile(r"Анимация\Анимация.exe")

    def Speak(self, text):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[3].id)
        self.engine.say(text)
        self.engine.runAndWait()

    def commandRu(self):
        try:
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    self.Start_Flag = True
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio_text = r.listen(source)
                    try:
                        text = r.recognize_google(audio_text, language="ru-RU").lower()
                    except sr.UnknownValueError:
                        self.start_and_end_animation()
                        text = self.commandRu()
                    return text
            except OSError:
                print(2)
        except AttributeError:
            self.Start_Flag = False
            self.start_and_end_animation()
            self.Speak("У вас не хватает библиотек")

    def get_drives(self):
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                self.drives.append(letter + ":\\")
            bitmask >>= 1

        return self.drives

    def search_music(self, drives, lookfor):
        for i in range(len(drives)):
            for root, dirs, files in os.walk(drives[i]):
                if lookfor in files:
                    key = join(root, lookfor)
                    self.write_music_to_json(key)
                    return key

    def get_shake(self):
        return self.shake

    def get_first(self):
        return self.first

    @staticmethod
    def write_music_to_json(music_path):
        key = os.path.split(music_path)
        temp = {
            "Name": key[1],
            "Path": music_path
        }
        with open("Files/music.json") as read_file:
            repeat = json.load(read_file)
            for item in repeat["music"]:
                if item['Name'] == key[1] and item['Path'] == music_path:
                    flag = True
                    break
                else:
                    flag = False
        if not flag:
            with open("Files/music.json", "a") as write_file:
                write_file.seek(write_file.truncate(write_file.tell() - 2))
                write_file.write(',\n')
                json.dump(temp, write_file)
                write_file.write(']}')

    def get_id_and_lenght_music(self, music_name):
        number = 1
        List = self.set_music()
        for i in range(len(List)):
            if number == int(music_name):
                self.max_music_id = number
                with open(self.file, "r") as music_path:
                    music_list = json.load(music_path)
                    for item in music_list["music"]:
                        if str(item['Name']) == List[i]:
                            self.music = MP3(item[r'Path'])
                            self.lenght_music = int(self.music.info.length)
                            break
                break
            number += 1
        return self.lenght_music, self.max_music_id

    def play_music(self, music_name):
        flag = False
        with open(self.file, "r") as music_path:
            music_list = json.load(music_path)
            for item in music_list["music"]:
                if str(item['Name']) == music_name:
                    th = threading.Thread(playsound(str(item[r'Path']), block=False))
                    th.daemon = True
                    th.run()
                    flag = True
        if not flag:
            playsound(self.search_music(self.get_drives(), music_name), block=False)

    def next_music_start(self, music_name, shake, first):
        if first:
            print(3)
            self.Play_Music(self.set_music(), music_name)
            self.next_music += 1
            self.first = False
        else:
            print(1)
            self.play_music(music_name)
            if not shake:
                if self.next_music == self.max_music_id:
                    self.next_music = 1
                    self.Play_Music(self.set_music(), self.next_music)
                else:
                    self.next_music += 1
                    self.Play_Music(self.set_music(), self.next_music)
            else:
                if self.lenght_music_buf == self.lenght_music:
                    if self.next_music == self.max_music_id:
                        self.next_music = 1
                        self.Play_Music(self.set_music(), self.musik_random[self.next_music])
                    else:
                        self.Play_Music(self.set_music(), self.musik_random[self.next_music])

    def music_forward_back(self, flag, shake, first):
        if flag and shake:
            print(1)
            self.next_music += 1
            self.next_music_start(self.next_music, shake=True, first=first)
        elif flag and not shake:
            print(2)
            self.next_music += 1
            self.next_music_start(self.next_music, shake=False, first=first)

        elif not flag and shake:
            print(3)
            self.next_music -= 1
            print(first)
            self.next_music_start(self.next_music, shake=True, first=first)

        else:
            print(4)
            self.next_music -= 1
            self.next_music_start(self.next_music, shake=False, first=first)

    def morphing(self, text):
        extractor = NumberExtractor()
        self.next_music = extractor.replace_groups(text)
        return extractor.replace_groups(text)

    def Play_Music(self, list, text):
        number = 1
        for i in range(len(list)):
            if number == int(text):
                self.play_music(list[i])
            number += 1

    def set_music(self):
        try:
            with open("../Files/music.json", "r") as file:
                temp = json.load(file)
                array = [row['Name'] for row in temp["music"]]
            return array
        except FileNotFoundError:
            self.Speak("Файл не найден")

    def shake_music(self):
        self.music_shake = []
        for i in range(len(self.set_music())):
            self.music_shake.append(i + 1)
        random.shuffle(self.music_shake)
        return self.music_shake

    def kill_music(self, lookfor):
        for process in (process for process in psutil.process_iter() if process.name() == lookfor):
            process.kill()

    def control_music(self, text):
        if "включи музыку" == text:
            # self.start_and_end_animation()
            self.Speak("Назовите номер песни")
            text = 3
            self.next_music_start(text, shake=False, first=True)
        elif "включи и перемешай музыку" == text:
            self.shake = True
            self.next_music_start(self.musik_random[0], shake=self.shake, first=True)
        elif "назад" in text:
            self.music_forward_back(flag=False, shake=self.shake, first=False)
        elif "вперёд" in text:
            self.music_forward_back(flag=True, shake=self.shake, first=True)
        elif "выключи музыку" in text:
            self.kill_music("Музыка.exe")
        elif "включи" in text:
            text = text.replace("включи", "")
            self.next_music_start(self.morphing(text), shake=self.shake, first=False)
        else:
            pass


class TimeLoop(threading.Thread):
    def run(self) -> None:
        while True:
            pass


def main():
    timeloop = TimeLoop()
    timeloop.start()
    music = Music()
    music.control_music("включи и перемешай музыку")
    time.sleep(3)
    print(444)
    music.control_music("назад")


if __name__ == '__main__':
    main()
