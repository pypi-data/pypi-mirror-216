# Auteur : Réda ID-TALEB

from .FailedVerdict import FailedVerdict

class FailedWhenExceptionExpectedVerdict(FailedVerdict):
    def __init__(self, filename:str, lineno, tested_line, expected_result, failure_message=""):
        super().__init__(filename, lineno, tested_line, expected_result, failure_message)

    def isSuccess(self):
        return False
    
    def get_details(self):
        common = "%s was not raised by %s" % (self.expected_result, self.tested_line)
        if self.details:
            
            common += "\n%s" % self.details
        return common

    def __str__(self):
        return super().__str__()