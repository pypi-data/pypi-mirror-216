from typing import List
from abc import *
from thonnycontrib.exceptions import NoFunctionSelectedToTestException
from thonnycontrib.utils import find_node
from .ast_parser import L1DocTest, L1TestAstParser
import ast

class TestFinderStrategy(ABC):
    """
    This is an implementation of the Strategy pattern. The strategies defines 
    the way that the ast nodes are extracted. 
    For example, the `FindAllStrategy` strategy will try to find all the ast nodes
    and extract them from the parsed source.
    
    All strategies rely on the AST module of python. The source is first analyzed 
    and all supported nodes are revealed, then each concrete strategy can find 
    its suitable nodes as needed. 
    """
    def __init__(self, filename="", source="", ast_parser:L1TestAstParser=None) -> None:
        self._ast_parser = L1TestAstParser(filename, source) if not ast_parser else ast_parser
    
    # ###### MAIN METHOD ###### #
    def find_docstrings(self) -> List[L1DocTest]:
        """Invoke this method to get the docstrings depending of the strategy.
        
        This method follows the Template Method pattern. It defines the common 
        algorithm for all concrete strategies. Then, it invokes the `_find_docstring()` 
        abstract method.
        
        Args:
            test_finder (TestFinder): The testFinder fo which the docstring 
            will be retrived.

        Returns:
            List[L1DocTest]: Returns a list of the L1DocTest. Each of L1DocTest 
            represents an AST node.
        """
        ast_nodes = self._ast_parser.get_supported_nodes()
        return self._find_docstring(ast_nodes)
    
    @abstractmethod
    def _find_docstring(self, ast_nodes: List[ast.AST]=[]) -> List[L1DocTest]:
        """Gets the docstrings from the source detained by the test_finder.

        Args:
            test_finder (TestFinder): An instance of TestFinder. The finder is used 
            to acces it's method to parse the content of the source.
            ast_nodes (List[ast.AST]): The source that is parsed by the TestFinder. 
            Default to empty list.
            
        Returns:
            (List[L1DocTest]): Returns a list of the L1DocTest. Each of L1DocTest 
            represents an AST node.
            
        Raises:
            The overriden methods could throw an exception. For each case, the raised 
            exceptions should be specified and explained into the docstrings.
        """
        pass

    def get_ast_nodes(self):
        return self._ast_nodes 
    
    def set_ast_nodes(self, ast_nodes):
        self._ast_nodes = ast_nodes
    
    def set_filename(self, filename):
        self._ast_parser.set_filename(filename)
    
    def set_source(self, source):
        self._ast_parser.set_source(source)
    
    
class FindAllL1DoctestsStrategy(TestFinderStrategy):
    def _find_docstring(self, ast_nodes):
        return self._ast_parser.get_l1doctests(ast_nodes)


class FindSelectedL1DoctestStrategy(TestFinderStrategy):
    def __init__(self, selected_line) -> None:
        super().__init__()
        self._selected_line = selected_line
    
    def _find_docstring(self, ast_nodes):
        """
        Note: The following docstring specifies only the raised excpetion.
        @See the docstring of the superclass to see the full docstring. 
            
        Raises:
            NoFunctionSelectedToTestException: When the selected line doesn' correspond to a 
            function or a class declaration.
        """
        selected_node = find_node(self._selected_line, ast_nodes)
        if not selected_node:
            msg = "%s\n\n%s" %  ("No function is selected to test !", 
                                 "The selected line must have a function or a class declaration.")
            raise NoFunctionSelectedToTestException(msg)
        return self._ast_parser.get_l1doctest(selected_node)
    
    def get_selected_line(self):
        return self._selected_line    
    
    def set_selected_line(self, selected_line):
        self._selected_line = selected_line   
        

class L1TestFinder:
    """
        The `TestFinder` relies on the `AST` module to parse the script and extracts 
        the nodes with their docstrings. 
        
        For each node, it invokes the `DoctestParser` to parse its docstring. Then, 
        for each dectected test, it associates an `Example` type that will contains 
        the `source`, `want` and the `line` of the test.
        
        Args:
            - filename(str): the filename of the source code.
            - source(str): the source code to be parsed by the `AST` parser and by the 
                    `DoctestParser`.
            - strategy(TestFinderStrategy): the strategy to use to find the docstrings.
    """
    def __init__(self, filename:str="", source:str="", strategy:TestFinderStrategy=None):      
        self._filename = filename
        self._source = source
        self._strategy = FindAllL1DoctestsStrategy(filename, source) if not strategy else strategy
    
    def extract_examples(self) -> List[L1DocTest]: 
        """
        Extract examples from the docstings of all the ast nodes of the source code.
        
        Returns a list of L1DocTest. Each of L1DocTest corresponds to an ast node.
        Each L1DocTest has it's list of `Example`
        
        Raises: 
            NoFunctionSelectedToTestException: when the selected line desn't refer to a 
            function/class signature.
            Error: A compilation error raised by the AST module.
            SpaceMissingAfterPromptException: when a space is missing after the prompt.
        """                
        return self._strategy.find_docstrings()
        
    def get_filename(self):
        return self._filename
    
    def set_filename(self, filename: str):
        self._filename = filename
        self._strategy.set_filename(filename)
    
    def get_source(self):
        return self._source
    
    def set_source(self, source: str):
        self._source = source
        self._strategy.set_source(source)
        
    def get_strategy(self):
        return self._strategy
    
    def set_strategy(self, strategy: TestFinderStrategy):
        self._strategy = strategy
        self._strategy.set_filename(self._filename)
        self._strategy.set_source(self._source)