import getpass

USER_NAME = getpass.getuser()


def add_to_startup():
    file_path = r"C:\Users\Ghou72rus\Desktop\Жора Трей.exe.lnk"
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)
        print(bat_path + '\\' + "open.bat")


def main():
    add_to_startup()


if __name__ == '__main__':
    main()


    def create_file(self):
        for i in range(len(self.create_files)):
            if self.create_files[i] == 1:
                with open("../Files/Language.txt", "w") as lan:
                    lan.write("Русский")
            elif self.create_files[i] == 2:
                with open("../Files/music.json", "w") as music:
                    music.write('"{music":"\n" [{"Name": "4.mp3", "Path": '
                                          r'"C:\\Users\\Ghou72rus\\Desktop\\4.mp3"}]}')
            elif self.create_files[i] == 3:
                with open("../Files/installed_files.txt", "w") as installed_files:
                    pass

            elif self.create_files[i] == 4:
                with open("../Files/requirements.txt", "w") as requirements:
                    requirements.write("natasha==0.10.0\nyargy==0.12.0\nPyQt5~=5.15.7\nExtractor~=0.5\nfuture~=0.18.2"
                                       "\npsutil~=5.9.1\nPyAutoGUI~=0.9.53\npyperclip~=1.8.2\npytesseract~=0.3.10\npyttsx3"
                                       "~=2.90\nwinapps~=0.2.0\nkeyboard~=0.13.5\nsimpleaudio~=1.0.4\nplaysound~=1.2.2"
                                       "\nPillow~=9.2.0")

    def check_files(self):
        try:
            with open("../Files/Language.txt") as lan:
                self.create_files.append(1)
            with open("../Files/music.json") as music:
                self.create_files.append(2)
            with open("../Files/installed_files.txt"):
                self.create_files.append(3)
            with open("../Files/requirements.txt"):
                self.create_files.append(4)
        except FileNotFoundError:
            self.Speak("Некоторые системные файлы отсутствуют, мне придется их создать")
            print(self.create_files)
            self.create_file()

      elif 'закрой' == text:
                self.start_and_end_animation()
                self.Speak("Что хотите закрыть?")
                self.operation_on_pc()
                from Script import List
                List.main("Files/tasklist.txt")
                id_task = self.change_word_to_number(self.commandRu())
                with open("Files/tasklist.txt", "r") as file:
                    array = [row.strip() for row in file]
                try:
                    self.close_file(array[id_task + 1])
                except TypeError:
                    self.start_and_end_animation()
                    self.Speak("Это не число!")
                    id_task = self.commandRu()
                finally:
                    try:
                        self.close_file(array[id_task + 1])
                    except TypeError:
                        self.start_and_end_animation()
                        self.Speak("Все равно не число!")
                        self.commandRu()