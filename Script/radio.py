import os
import threading
import time

import psutil
import pyttsx3
import speech_recognition as sr

try:
    vlc_flag = True
    os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')
    import vlc
except FileNotFoundError:
    vlc_flag = False


class Radio:
    def __init__(self):
        self.counter = 0
        self.radio_list = []
        self.radio_list_source = []
        try:
            self.instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
            self.player = self.instance.media_player_new()
        except:
            self.Speak("У вас не установлен медиаплеер VLC")

    def write_source(self):
        try:
            with open("Files/radio_station.txt", "r") as file:
                array = [row.strip().split(" | ") for row in file]
            for i in range(len(array)):
                index = len(array[i])
                if index <= 1:
                    pass
                else:
                    for j in range(index):
                        if j == 0:
                            self.radio_list.append(array[i][0])
                        else:
                            self.radio_list_source.append(array[i][1])
        except FileNotFoundError:
            self.Speak("файла со списком радио не существует, сейчас я его создам")
            with open("Files/radio_station.txt", "w") as file:
                pass

    def play_radio(self, radio_list):
        for i in range(len(self.radio_list)):
            if self.radio_list[i].lower() == radio_list:
                self.media = self.instance.media_new(self.radio_list_source[i])
                self.player.set_media(self.media)
                self.player.play()
                time.sleep(1)
                if self.player.is_playing() > 0:
                    self.counter = i
                    break
                else:
                    self.Speak("не удалось подключиться к радиостанции, попробуйте сказать другую")
                    text = self.commandRu()
                    return self.check_radio(text)

    def pause_radio(self):
        self.player.pause()

    def stop_radio(self):
        self.player.stop()

    def repeat_radio_start(self):
        self.player.play()

    def next_radio(self):
        if self.counter >= len(self.radio_list_source) - 1:
            self.counter = 0
            self.media = self.instance.media_new(self.radio_list_source[self.counter])
            self.player.set_media(self.media)
            self.player.play()
        else:
            self.counter += 1
            self.media = self.instance.media_new(self.radio_list_source[self.counter])
            self.player.set_media(self.media)
            self.player.play()

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
                        text = self.commandRu()
                    return text
            except OSError:
                pass
        except AttributeError:
            pass

    def Speak(self, text):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[3].id)
        self.engine.say(text)
        self.engine.runAndWait()

    def show_content(self):
        os.startfile("Список радио/Список радио.exe")

    def close_content(self):
        for process in (process for process in psutil.process_iter() if process.name() == "Список радио.exe"):
            process.kill()

    def control_radio(self, text):
        if text == "включи":
            self.repeat_radio_start()
        elif text == "пауза":
            self.pause_radio()
        elif text == "выключи":
            self.stop_radio()
        elif text == "переключи":
            self.next_radio()
        elif "включи" in text:
            text = text.replace("включи ", '')
            self.check_radio(text)
        elif "покажи список" in text:
            self.show_content()
        elif "убери список" in text:
            self.close_content()

    def check_radio(self, text):
        flag = True
        for i in range(len(self.radio_list)):
            if text == self.radio_list[i].lower():
                print(self.radio_list[i].lower())

                flag = False
                self.play_radio(text)
                break
        if flag:
            self.Speak("Такого радио нет в списке, скажите еще раз")
            text = self.commandRu()
            return self.check_radio(text)


class Waiter(threading.Thread):
    def run(self):
        while True:
            pass


def main():
    if vlc_flag:
        radio = Radio()
        radio.show_content()
        radio.write_source()
        radio.Speak("что хотите включить?")
        waiter = Waiter()
        waiter.start()
        radio_start = radio.commandRu()
        radio.check_radio(radio_start)
        while True:
            text = radio.commandRu()
            radio.control_radio(text)
    else:
        Radio()


if __name__ == '__main__':
    main()
