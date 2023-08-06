# Module Evaluator

from typing import List

from thonnycontrib.utils import send_current_state
from .ast_parser import L1DocTest
from thonnycontrib.properties import FINISHED_STATE
from thonnycontrib.exceptions import *
from thonnycontrib.utils import *
from .doctest_parser import *
from thonny import *
from types import ModuleType
from .test_finder import L1TestFinder, TestFinderStrategy
import sys 

class Evaluator:
    """
    Instantiate an `Evaluator` with a filename, a source and a test_finder. 
    The evaluator relies on the `TestFinder` to parse and extracts the tests from
    the docstrings. 
    
    Args:
        filename (str, optional): the filename to be executed by the `Evaluator`. Defaults to "".
        source (str, optional): the source code to be parsed by the `TestFinder`. Defaults to "".
        test_finder (TestFinder, optional): the finder of the tests declared in docstrings. 
                                        Defaults to TestFinder().
    """
    def __init__(self, filename:str="", source:str="", test_finder=L1TestFinder()):
        self._globals = dict()
        self._module: ModuleType = None
        self._test_finder: L1TestFinder = test_finder
        self._test_finder.set_filename(filename)
        self._test_finder.set_source(source)

    def evaluate(self) -> List[L1DocTest]:
        """Imports the module from the filename, sets the global variables to
        imported module's dict and then evaluates the tests.

        Returns:
            List[L1DocTest]: Returns for each node its list of verdicts (type of Test)
        """
        # si le `self._module` est null, alors `Evaluator` va s'occuper d'importer lui même
        # le module à partir du filename. 
        # Sinon, le module a été fournit, donc `Evaluator` utilisera le module fournit.
        if not self._module:
            # The `import_module()` function can raise an exception(see it's doc)
            self._module = import_module(self.get_filename()) 
        
        # set a globals dictionary that will contains all the functions and 
        # meta-informations decalared in the module
        self.set_global_variables_to_module_ones()
        return self.__evaluate_l1doctests() 
    
    def __evaluate_l1doctests(self) -> List[L1DocTest]:
        """
        Evaluate all the extracted l1doctests containing in the source code.
        
        Args:
            module (ModuleType): The module to be run.
        
        Returns:
            List[L1DocTest]: Returns the list of the evaluated l1doctests. 
            The verdicts are already computed and contained in each of the L1doctest.
        
        Raises:
            NoTestFoundException: When no test are found in the working editor.
            CompilationError: When the doctest parser raises an exception, it's catched 
                            and raised as a `CompilationError`, or when AST parser fails.
        """
        try:     
            # This line parses the source using the AST module and can raise a compilation error 
            l1doctests = self._test_finder.extract_examples() 
            for l1doctest in l1doctests: 
                self.set_global_variables_to_module_ones()
                l1doctest.evaluate(self.get_globals())
            send_current_state(state=FINISHED_STATE) # tells that the evaluation is finished
            return l1doctests
        except NoFunctionSelectedToTestException as e:
            raise RuntimeException(str(e))
        except DoctestParserException as e:
            raise CompilationError(str(e)) 
        except BaseException as e:
            # the compilation error is catched and raised as a CompilationError
            # and the evaluation is interrupted(because we cannot parse a content
            # with compilation errors).
            error_info = sys.exc_info()
            formatted_error = get_last_exception(error_info)
            raise CompilationError(formatted_error)      
    
    def get_globals(self):
        return self._globals

    def get_module(self):
        return self._module

    def set_module(self, module: ModuleType):
        self._module = module
        
    def set_global_variables_to_module_ones(self):
        '''Set self._globals to module __dict__ using a shallow copy like
        doctest does.
        '''
        self._globals = self._module.__dict__.copy()
        
    def set_test_finder(self, test_finder):
        self._test_finder = test_finder
    
    def get_test_finder(self):
        return self._test_finder

    def set_filename(self, filename):
        self._test_finder.set_filename(filename)
    
    def get_filename(self):
        return self._test_finder.get_filename()
    
    def set_source(self, source:str):
        self._test_finder.set_source(source)
        
    def get_source(self):
        return self._test_finder.get_source()
    
    def set_finder_strategy(self, finder_strategy: TestFinderStrategy):
        self._test_finder.set_strategy(finder_strategy)


