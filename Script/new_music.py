import os
import threading

try:
    vlc_flag = True
    os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
    import vlc
except FileNotFoundError:
    vlc_flag = False

import json
import os
import random
import string
from ctypes import windll
from os.path import join
import psutil
from mutagen.mp3 import MP3
from extractor import NumberExtractor
import pyttsx3
import speech_recognition as sr


class Music(object):
    def __init__(self):
        try:
            self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
            self.player = self.instance.media_player_new()
        except():
            self.Speak("У вас не установлен медиаплеер VLC")
        self.first = True
        self.shake = False
        self.music_shake = []
        self.musik_random = self.shake_music()
        self.next_music: int = 0
        self.lenght_music = 0
        self.music: int = 0
        self.lenght_music_buf = 0
        self.drives = []
        self.max_music_id = len(self.set_music())
        self.file = "../Files/music.json"
        self.kill_flag = False

    def __del__(self):
        pass

    def start_and_end_animation(self):
        try:
            os.startfile(r"Анимация\Анимация.exe")
        except FileNotFoundError:
            self.Speak("У вас нет анимации")

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
                pass
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

    def get_lenght(self):
        return self.lenght_music

    def set_music_lenght(self, music_name):
        self.lenght_music, _ = self.get_id_and_lenght_music(music_name)

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
        self.max_music_id = len(List)
        return self.lenght_music, self.max_music_id

    def play_music(self, music_name):
        flag = False
        with open(self.file, "r") as music_path:
            music_list = json.load(music_path)
            for item in music_list["music"]:
                if str(item['Name']) == music_name:
                    self.media = self.instance.media_new(item['Path'])
                    self.player.set_media(self.media)
                    self.player.play()
                    flag = True
        if not flag:
            self.media = self.instance.media_new(music_name)
            self.player.set_media(self.search_music(self.get_drives(), music_name))
            self.player.play()

    def next_music_start(self, music_name, shake, next, first):
        if first:
            self.Play_Music(self.set_music(), music_name)
        else:
            if not shake:
                if next:
                    if music_name == self.max_music_id or music_name < 0:
                        self.next_music = 1
                        self.Play_Music(self.set_music(), self.next_music)
                    else:
                        self.Play_Music(self.set_music(), self.next_music)
                else:
                    if music_name == self.max_music_id:
                        self.next_music = 1
                        self.Play_Music(self.set_music(), self.next_music)
                    else:
                        self.next_music += 1
                        self.Play_Music(self.set_music(), self.next_music)
            else:
                if next:
                    if music_name == self.max_music_id or music_name < 0:
                        self.next_music = 1
                        self.Play_Music(self.set_music(), self.musik_random[self.next_music])
                    else:
                        self.Play_Music(self.set_music(), self.musik_random[music_name])

                else:
                    if music_name == self.max_music_id or music_name < 0:
                        self.next_music = 1
                        self.Play_Music(self.set_music(), self.musik_random[self.next_music])
                    else:
                        self.Play_Music(self.set_music(), self.musik_random[music_name])

    def music_forward_back(self, flag, shake):
        if flag and shake:
            self.next_music += 1
            self.next_music_start(self.next_music, shake=True, next=True, first=self.first)
        elif flag and not shake:
            self.next_music += 1
            self.next_music_start(self.next_music, shake=False, next=True, first=self.first)

        elif not flag and shake:
            self.next_music -= 1
            self.next_music_start(self.next_music, shake=True, next=True, first=self.first)

        else:
            self.next_music -= 1
            self.next_music_start(self.next_music, shake=False, next=True, first=self.first)

    def morphing(self, text):
        extractor = NumberExtractor()
        self.next_music = int(extractor.replace_groups(text))
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

    def show_content(self):
        os.startfile("Список музыки.exe")

    def close_content(self):
        self.kill_music("Список музыки.exe")

    def control_music(self, text):
        if "включи музыку" == text:
            self.start_and_end_animation()
            self.Speak("Назовите номер песни")
            text = self.morphing(self.commandRu())
            self.set_music_lenght(text)
            self.next_music_start(text, shake=self.shake, next=False, first=self.first)
            self.first = False
        elif "включи и перемешай музыку" in text:
            self.shake = True
            self.music_shake = self.shake_music()
            self.next_music_start((self.music_shake[0]), shake=self.shake, next=False, first=self.first)
            self.first = False
        elif "назад" in text:
            self.music_forward_back(flag=False, shake=self.shake)
        elif "вперёд" in text:
            self.music_forward_back(flag=True, shake=self.shake)
        elif "выключи музыку" in text:
            self.kill_music("Музыка.exe")
        elif "включи" in text:
            self.first = False
            text = int(self.morphing(text.replace("включи", "")))
            self.next_music_start(text, shake=self.shake, next=False, first=self.first)
        elif "убери список" in text:
            self.close_content()
        elif "покажи список" in text:
            self.show_content()
        else:
            pass

    def Start(self):
        while True:
            self.control_music(self.commandRu())


class Waiter(threading.Thread):
    def run(self):
        while True:
            pass


def main():
    music = Music()
    music.show_content()
    Waiter.start(Waiter())
    while True:
        music.control_music(music.commandRu())


if __name__ == '__main__':
    main()
