from .ExampleVerdict import ExampleVerdict

class SetupVerdict(ExampleVerdict):
    def __init__(self, filename, lineno, tested_line):
        super().__init__(filename, lineno, tested_line, "None")

    def get_color(self):
        return ""

    def isSuccess(self):
        return True
    
    def __str__(self):
        return "Setup succeed for: %s " % (self.tested_line)