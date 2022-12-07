import datetime
import threading

import psutil


class KillSecondProcces(threading.Thread):
    def __init__(self):
        super().__init__()
        self.time_started = []
        self.process_name = []

    def run(self) -> None:

        while True:
            process_name_time = []
            i = 0
            for process in (process for process in psutil.process_iter()):
                PROCCES = str(process)
                PROCCES = PROCCES.split(",")
                try:

                    if "Анимация.exe" == process.name() or "Жора.exe" == process.name() or "Радио.exe" == process.name() or "Музыка.exe" == process.name() \
                            or "Жора Трей.exe" == process.name() or "Запись.exe" == process.name() or "Список " \
                                                                                                      "музыки.exe" == \
                            process.name() or "Список радио.exe" == process.name() or "Камера.exe" == process.name() \
                            or "Чтение документа.exe" == process.name():
                        self.process_name.append(process.name())
                        self.time_started.append(
                            PROCCES[3].replace("started=", "").replace("'", "").replace(")", '').strip())
                        process_name_time.append(
                            [process.name(),
                             PROCCES[3].replace("started=", "").replace("'", "").replace(")", '').strip()])
                        i += 1

                except:
                    continue
            process_name_time = sorted(process_name_time)
            for i in range(len(process_name_time)):
                try:
                    if process_name_time[i][0] == process_name_time[i + 1][0] and datetime.datetime.strptime(
                            process_name_time[i][1],
                            '%H:%M:%S') < datetime.datetime.strptime(process_name_time[i + 1][1], '%H:%M:%S'):
                        del process_name_time[i]
                except IndexError:
                    break

            print(process_name_time)
            for i in range(len(process_name_time)):
                for process in (process for process in psutil.process_iter()):
                    try:
                        if process_name_time[i][1] != datetime.datetime.fromtimestamp(process.create_time()).strftime(
                                '%H:%M:%S') and process_name_time[i][0] == process.name():
                            process.kill()
                            break
                    except IndexError:
                        break


if __name__ == '__main__':
    KillSecondProccess = KillSecondProcces()
    KillSecondProccess.start()
