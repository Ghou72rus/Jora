import datetime
import threading
import time
import pyttsx3


class ToDo:
    def Speak(self, text):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.name == "Artemiy":
                self.engine.setProperty('voice', voice.id)
                self.engine.setProperty('rate', 160)
        self.engine.say(text)
        self.engine.runAndWait()

    @staticmethod
    def create_todo(todo_text):
        with open("Files/todo.txt", "a") as todo_write:
            todo_text += "\n"
            todo_write.writelines(todo_text)

    @staticmethod
    def read_todo():
        todo = []
        with open("../Files/todo.txt", "r") as todo_read:
            todo += todo_read.readlines()
        return todo

    def check_todo(self):
        todo_time = []
        todotext = []
        temp = ""
        now = str(datetime.datetime.now().replace(second=0, microsecond=0))
        with open("Files/todo.txt", "r") as todo_check:
            todo = todo_check.readlines()
        for item in todo:
            todo_text = item.split()
            item = item.split()
            todo_time.append(item[-2] + " " + item[-1])
            todo_text.pop()
            todo_text.pop()
            for i in range(len(todo_text)):
                temp += todo_text[i] + " "
            todotext.append(temp)
            temp = ""
        for i in range(len(todo_time)):
            if todo_time[i] == now:
                self.Speak("напоминаю вам, что вы хотели" + todotext[i])


class Waiter(threading.Thread):
    def run(self):
        todo = ToDo()
        while True:
            todo.check_todo()
            time.sleep(60)


def main():
    waiter = Waiter()
    waiter.start()


if __name__ == '__main__':
    main()
