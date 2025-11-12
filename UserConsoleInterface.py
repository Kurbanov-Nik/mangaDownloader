from ConsoleIntermediary import ConsoleIntermediary

class ConsoleInterface:
    def __init__(self):
        self.mediator = ConsoleIntermediary()

    def start(self):
        print("---///   Начало работы   ///---")
        while True:
            entry = input("Укажите ссылку на мангу: ")
            break
        print(r"---\\\ Завершение работы \\\---")


if __name__ == "__main__":
    a = ConsoleInterface()
    a.start()