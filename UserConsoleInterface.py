from ConsoleIntermediary import ConsoleIntermediary

class ConsoleInterface:
    def __init__(self):
        self.mediator = ConsoleIntermediary()

    def start(self):
        print("---///   Начало работы   ///---")
        while True:
            entry = input("Укажите ссылку на мангу: ")
            if not self.mediator.validateURL(entry):
                continue
            self.mediator.setupDownloader()
            if not self.mediator.checkConnection():
                continue
            break
        print(r"---\\\ Завершение работы \\\---")


if __name__ == "__main__":
    a = ConsoleInterface()
    a.start()