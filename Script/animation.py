import os
import threading
import time
import tkinter as tk

import psutil
from PIL import Image, ImageTk
from itertools import count


class Waiter(threading.Thread):
    def run(self):
        time.sleep(3)
        kill_start("Анимация.exe")


def kill_start(lookfor):
    for process in (process for process in psutil.process_iter() if process.name() == lookfor):
        process.kill()


class ImageLabel(tk.Label):

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def start_animation():
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", root.iconify)
    root.bind('<Escape>', lambda e: root.destroy())
    TRNAS_COLOR = '#abcdef'
    root.overrideredirect(True)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.attributes('-transparentcolor', TRNAS_COLOR)
    root.title("animation")
    tk.Label(root, bg=TRNAS_COLOR).pack()
    lbl = ImageLabel(root)
    lbl.pack()
    try:
        lbl.load('Files\mygif.gif')
        root.mainloop()
    except FileNotFoundError:
        print("Нет файла")


def main():
    waiter = Waiter()
    waiter.start()
    th = threading.Thread(start_animation())
    th.start()


if __name__ == '__main__':
    main()
