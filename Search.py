import time
import keyboard
import pyautogui
import pyperclip
import pyttsx3
from time import sleep
import speech_recognition as sr
from keyboard import press_and_release


class Save(object):
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

    @staticmethod
    def paste(text):
        pyperclip.copy(text)
        press_and_release('ctrl + v')

    def type(self, text, interval=0.2):
        buffer = pyperclip.paste()
        try:
            if not interval:
                self.paste(text)
            else:
                for char in text:
                    self.paste(char)
                    sleep(interval)
            pyperclip.copy(buffer)
        except TypeError:
            pass

    @staticmethod
    def SearchObject(path):
        point = pyautogui.locateOnScreen(path)
        return point

    @staticmethod
    def MoveMouse(point):
        pyautogui.click(point, duration=0.5)
        sleep(1)

    def write_message(self):
        self.Speak("Скажите что мне написать")
        while True:
            text = self.commandRu()
            if text != "сохрани":
                self.type(text + " ", 0.2)
                sleep(1)
            else:
                break

    def SaveFile(self, name):
        keyboard.press_and_release("ctrl + s")
        time.sleep(1)
        self.type(name, 0.2)
        time.sleep(1)
        keyboard.press_and_release("enter")

    def Start(self):
        self.write_message()
        self.Speak("Скажите как мне его назвать")
        name = self.commandRu()
        self.SaveFile(name)


def main():
    save = Save()
    save.Start()


if __name__ == '__main__':
    main()
