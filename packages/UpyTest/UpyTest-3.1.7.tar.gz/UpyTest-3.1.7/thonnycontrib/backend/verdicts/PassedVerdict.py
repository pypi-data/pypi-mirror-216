# Auteur : Esteban COLLARD, Nordine EL AMMARI

from .ExampleVerdict import ExampleVerdict

class PassedVerdict(ExampleVerdict):
    def __init__(self, filename, lineno, tested_line, expected_result):
        super().__init__(filename, lineno, tested_line, expected_result)

    def get_color(self):
        return "green"

    def isSuccess(self):
        return True
    
    def __str__(self):
        return "Test OK for: %s " % (self.tested_line)