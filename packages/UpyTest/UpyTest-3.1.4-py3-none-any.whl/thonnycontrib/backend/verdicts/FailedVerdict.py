# Auteur : Esteban COLLARD, Nordine EL AMMARI

from .ExampleVerdict import ExampleVerdict

class FailedVerdict(ExampleVerdict):
    def __init__(self, filename:str, lineno, tested_line, expected_result, real_result):
        super().__init__(filename, lineno, tested_line, expected_result, real_result)
 
    def get_color(self):
        return "red"

    def isSuccess(self):
        return False
    
    def get_details(self):
        want, got = self.expected_result, self.details
        
        if isinstance(got, str): # "''"
            got = "\'\'" if got == str() else "\'%s\'" % got
        return 'Expected: %s, Got: %s' % (want, got)
    
    def __str__(self):
        return "Test failed for: %s" % (self.tested_line)