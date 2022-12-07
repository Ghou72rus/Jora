from tkinter import filedialog
import tkinter as tk

import pyttsx3


class speak_file:
    def Speak(self, text):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == "Artemiy":
                self.engine.setProperty('voice', voice.id)
                self.engine.setProperty('rate', 160)
        self.engine.say(text)
        self.engine.runAndWait()

    def selectCustomerFileTK(self):
        root = tk.Tk()
        root.wm_attributes('-topmost', 1)
        root.withdraw()
        filename = filedialog.askopenfilename()

        return filename

    def speak_document(self):
        import docx2txt
        from PyPDF2 import PdfReader
        filename = self.selectCustomerFileTK()
        if 'docx' in filename:
            try:
                text = docx2txt.process(filename)
                print(text)
                self.Speak(text)
            except:
                self.Speak("Неверный формат файла. Возможно вы не так его сохранили.")
        elif 'pdf' in filename:
            text = ''
            reader = PdfReader(filename)
            number_of_pages = len(reader.pages)
            print(number_of_pages)
            for i in range(number_of_pages):
                page = reader.pages[i]
                try:
                    text += page.extract_text()
                except UnicodeDecodeError:
                    print("Страница номер " + str(i) + " нераспознана из-за специальных символов")
            self.Speak(text)
        else:
            buf = ''
            try:
                with open(filename, "r") as f:
                    array = [row.strip() for row in f]
                for i in range(len(array)):
                    buf += array[i] + " "
                print(buf)
                self.Speak(buf)
            except UnicodeDecodeError:
                self.Speak("Неверный формат файла!")
            except FileNotFoundError:
                pass


if __name__ == '__main__':
    sf = speak_file()
    sf.speak_document()
