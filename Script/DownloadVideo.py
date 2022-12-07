import threading
import time
import pyperclip
import pyttsx3
import pytube


class DownloadVideo(threading.Thread):
    def Speak(self, text):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == "Artemiy":
                self.engine.setProperty('voice', voice.id)
                self.engine.setProperty('rate', 160)
        self.engine.say(text)
        self.engine.runAndWait()

    def run(self):
        self.Speak("Пожалуйста скопируйте ссылку")

        link = pyperclip.paste()
        while True:
            if 'youtube' in link:
                self.Speak('Загрузка началась')
                break
            else:
                self.Speak("Неверная ссылка")
                time.sleep(5)
                link = pyperclip.paste()
        yt = pytube.YouTube(link)
        stream = yt.streams.order_by('resolution').filter(progressive=True).desc().first()
        try:
            stream.download('Download/')
            self.Speak("Загрузка завершена")
        except:
            self.Speak("Неудалось скачать видео")
            pass


if __name__ == '__main__':
    DV = DownloadVideo()
    DV.start()
