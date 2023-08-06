# Auteur : Esteban COLLARD, Nordine EL AMMARI
# Refactored by Manal LAGHMICH & Réda ID-TALEB
# Last refactored by Réda ID-TALEB

from abc import ABC, abstractmethod

class ExampleVerdict(ABC):
    def __init__(self, filename:str, lineno:int, tested_line:str, expected_result:str, details:str=""):
        """
        Build an instance of a verdict. A the Test object represents a result of a 
        tested line in a docstring.
        
        Args:
            filename (str): The filename in wich the tests are run.
            lineno (int): The line number of the tested line.
            tested_line (str): The tested line.
            expedted_result (str): The expected result of the tested line.
            details (str): Other details that may be added to the verdict.
        """
        self.filename = filename
        self.lineno = lineno
        self.tested_line = tested_line.strip("\n").strip()
        self.expected_result = expected_result.strip("\n").strip()
        self.details = details
    
    @abstractmethod
    def get_color(self) -> str:
        """The color of the verdict."""
        pass
    
    @abstractmethod
    def isSuccess(self) -> bool:
        """Returns True if the verdict is a success, False otherwise."""
        pass
    
    @staticmethod
    def get_verdicts_by_priority():
        from .ExceptionVerdict import ExceptionVerdict
        from .PassedVerdict import PassedVerdict
        from .FailedVerdict import FailedVerdict
        from .FailedWhenExceptionExpectedVerdict import FailedWhenExceptionExpectedVerdict
        return [ExceptionVerdict,
                FailedWhenExceptionExpectedVerdict, 
                FailedVerdict, 
                PassedVerdict]
    
    ## Getters ##
    def get_tested_line(self):
        return self.tested_line

    def get_expected_result(self):
        return self.expected_result
    
    def get_details(self):
        return self.details
    
    def get_filename(self):
        return self.filename
    
    def get_lineno(self):
        return self.lineno