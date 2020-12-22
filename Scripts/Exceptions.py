class ExcelReadException(Exception):
    demo = "Can not read {} successfully"
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return ExcelReadException.demo.format(self.name)

class MsgException(Exception):
    def __init__(self, value:str="Unknown Exception"):
        self.value = value

    def __str__(self):
        return self.value