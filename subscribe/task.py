from subscribe.abstracts.ISubscribe import ITask


class MyCustomExampleTask(ITask):

    def __init_(self, name=""):
        self.name = name

    def __custom_func(self):
        print(f"Run Custom Func Success...... {self.name}")

    def run(self) -> None:
        print("Start Task...")
        self.__custom_func()
        