"""import ctypes

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

titles = []


def foreach_window(hwnd, lParam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        GetWindowText(hwnd, buff, length + 1)
        titles.append(buff.value)
    return True


EnumWindows(EnumWindowsProc(foreach_window), 0)


def main():
    for t in titles:
        print(t)
    return titles


if __name__ == '__main__':
    main()

# Писалка сообщений дебаг
# def WriteMessage():
# def SearchObject():
Cordinate = pyautogui.locateOnScreen(r"C:\Users\Ghou72rus\Desktop\girlfrend.png")
return Cordinate
point = SearchObject()
   def WriteMessage(self):
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
        self.start_and_end_animation()
        self.Speak("Что написать?")
        Message = self.commandRu()
        typing(Message, 0.1)
        self.start_and_end_animation()
        self.Speak("Отправить?")
        Answer = self.commandRu()
        while Answer != 'да':
            Answer = self.commandRu()

        if 'да' in Answer:
            point = pyautogui.locateOnScreen(r"C:\Users\Ghou72rus\Desktop\Enter.png")
            pyautogui.click(point, duration=0.5)
        else:
            pass


            elif 'напиши сообщение' in text:
                self.WriteMessage()

            """
from multiprocessing.connection import Listener
from time import sleep

from PIL import ImageGrab


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
