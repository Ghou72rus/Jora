import os
import time
import psutil as psutil
import pyttsx3
import speech_recognition as sr


class Start_Jora:
    def __init__(self):
        self.flag = True

    def Speak(self, text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if voice.name == "Artemiy":
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', 160)
        engine.say(text)
        engine.runAndWait()

    def start_jora(self):
        try:
            r = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio_text = r.listen(source)
                    try:
                        text = r.recognize_google(audio_text, language="ru-RU").lower()
                        return text
                    except:
                        pass
            except OSError:
                pass
        except AttributeError:
            pass

    def kill_start_jora(self, lookfor):
        for process in (process for process in psutil.process_iter() if process.name() == lookfor):
            process.kill()

    def Start(self):
        while True:
            text = self.start_jora()
            try:
                if "привет жора" in text:
                    try:
                        os.startfile("Жора.exe")
                        time.sleep(5)
                        self.kill_start_jora('Жора трей')
                    except FileNotFoundError:
                        self.Speak("Кажется, у вас не установлен голосовой помощник Жора")
            except TypeError:
                pass


def main():
    jora = Start_Jora()
    jora.Start()


if __name__ == '__main__':
    main()
