import ast
from enum import Enum 
from .verdicts.ExceptionVerdict import ExceptionVerdict
from .verdicts.FailedVerdict import FailedVerdict
from .verdicts.ExampleVerdict import ExampleVerdict
from ..properties import EXECUTED_STATE, PENDING_STATE
from ..utils import create_node_representation, send_current_state
from .doctest_parser import DocTestParser, Example
from typing import List, Tuple

# Only these types can have a docstring 
# according to ast's module documentation
SUPPORTED_TYPES = (ast.FunctionDef, 
                   ast.AsyncFunctionDef, 
                   ast.ClassDef, 
                   ast.Module)

class L1DocTestFlag(Enum):
    """This enum represents the flag of an L1DocTest. A flag is an integer that 
    represents the global verdict of the L1DocTest. 
    
    The flag can be one of the following: `FAILED_FLAG`, `EMPTY_FLAG`, `PASSED_FLAG`.
    """
    FAILED_FLAG = -1
    EMPTY_FLAG = 0
    PASSED_FLAG = 1
    
    def from_value(value: int):
        """This method returns the flag corresponding to the given value."""
        if value not in [-1, 0, 1]:
            raise ValueError("The value must be one of the following: -1, 0, 1")
        if value == -1:
            return L1DocTestFlag.FAILED_FLAG
        elif value == 0:
            return L1DocTestFlag.EMPTY_FLAG
        else:
            return L1DocTestFlag.PASSED_FLAG
    
    def get_image(self):
        """This method returns the icon corresponding to the flag."""
        if self.value == -1:
            return "failed.png"
        elif self.value == 0:
            return "warning.png"
        else:
            return "passed.png"
    
    def get_color(self):
        """This method returns the color corresponding to the flag."""
        if self.value == -1:
            return "red"
        elif self.value == 0:
            return "orange"
        else:
            return "green"
        
    def short_name(self):
        """This method returns the text corresponding to the flag."""
        if self.value == -1:
            return "Failed"
        elif self.value == 0:
            return "Empty"
        else:
            return "Passed"
    
    @staticmethod
    def get_priorities():
        return [L1DocTestFlag.FAILED_FLAG, L1DocTestFlag.PASSED_FLAG, L1DocTestFlag.EMPTY_FLAG]
    
    def should_expand(self):
        """Return True if the flag requirs to expand the node."""
        return self.value == -1 
    
    
class L1DocTest():
    """
    An `L1DocTest` is associated to an ast node and that groups its tests 
    containing in the docstring of that node.
    The `L1DocTest` is identified by its node, its docstring, its starting 
    lineno and its ending lineno. The starting/ending lineno is the starting/ending 
    line of the docstring. 
    
    An `L1DocTest` handles a list of the example of type `Example`.
    
    Args:
        name (str): The name of the L1Doctest. The name is always the name 
        of it's associated ast node.
        node_lineno (int): The line of the associated ast node.
        start_lineno (int): the starting lineno of the docstring.
        Defaults to -1 If no docstring was found.
        end_lineno (int): the ending lineno of the docstring.
        Defaults to -1 If no docstring was found.
    """
    def __init__(self, filename:str, name:str, node_lineno:int, start_lineno=-1, end_lineno=-1) -> None:
        self.__filename = filename
        self.__name = name
        self.__node_lineno = node_lineno
        self.__start_lineno = start_lineno
        self.__end_lineno = end_lineno
        self.__examples:List[Example] = []
        self.__flag: L1DocTestFlag = None  # The global verdict of the l1doctest. 
                                           # Set as None while the l1doctest is not evaluated.
    
    def evaluate(self, globs:dict):
        """
        Evaluate the examples of this L1Doctest. Each example is evaluated and its 
        verdict is setted. The global verdict of the L1Doctest is also setted and you
        could access it by calling the method L1Doctest.get_flag().
        
        Args:
            globs (dict): The globals of the module in wich the L1Doctest is defined.
        Returns:
            L1DocTestFlag: The global verdict of the L1Doctest.
        """
        for example in self.get_examples(): 
            send_current_state(state=PENDING_STATE, source=example.source.strip(), invite=example.invite, lineno=example.lineno)
            example.compute_and_set_verdict(globs) 
            send_current_state(state=EXECUTED_STATE)
        self.__flag = self.__get_global_flag() # set the global verdict of the l1doctest 
        return self.__flag
        
    def __get_global_flag(self) -> L1DocTestFlag:
        """
        This method should be invoked after the evaluation (evaluate_examples() method) 
        of the l1doctest. It returns a flag that represents the global verdict of the L1Doctest.
        
        Returns:
            L1DocTestFlag: returns a flag that represents the global 
            verdict of the l1doctest. Return None if the l1doctest is not evaluated.
        """
        # on s'assure que les tests sont évalués. càd qu'il y a au moins un verdict.
        if not self.is_evaluated():
            return None
        if not self.has_examples():
            return L1DocTestFlag.EMPTY_FLAG
        elif self.has_only_setUps() and all([ex.get_verdict().isSuccess() for ex in self.__examples]):
            return L1DocTestFlag.EMPTY_FLAG
        elif all([ex.get_verdict().isSuccess() for ex in self.__examples]):
            return L1DocTestFlag.PASSED_FLAG
        else:
            return L1DocTestFlag.FAILED_FLAG

    def is_evaluated(self):
        """Returns True if the L1Doctest is evaluated. Otherwise, returns False."""
        return all(ex.is_evaluated() for ex in self.__examples)
    
    ## Stats methods ##
    def count_tests(self):
        """
        Count the number of the tests containing in this L1doctest. The setups
        are not considered in the counting.
        
        Returns:
            int: the number of the tests containing in the l1doctest.
        """ 
        return sum([1 for ex in self.__examples if ex.is_a_test()])
    
    def count_setups(self):
        """
        Count the number of the setups containing in this L1doctest. The tests
        are not considered in the counting.
        
        Returns:
            int: the number of the setups containing in the l1doctest.
        """ 
        return sum([1 for ex in self.__examples if not ex.is_a_test()])
    
    def count_passed_tests(self):
        """Count the number of passed tests. Return `None` if the L1Doctest is not evaluated."""
        if not self.is_evaluated():
            return None
        return sum([1 for ex in self.__examples if ex.is_a_test() and ex.get_verdict().isSuccess()])
    
    def count_failed_tests(self):
        """Count the number of failed tests. Return `None` if the L1Doctest is not evaluated."""
        if not self.is_evaluated():
            return None
        return sum([1 for ex in self.__examples if not ex.get_verdict().isSuccess() and isinstance(ex.get_verdict(), FailedVerdict)])
    
    def count_error_tests(self):
        """
        Count the number of tests that raised an exception.
        Return `None` if the L1Doctest is not evaluated
        """
        if not self.is_evaluated():
            return None
        return sum([1 for ex in self.__examples if not ex.get_verdict().isSuccess() and isinstance(ex.get_verdict(), ExceptionVerdict)])
    
    ## Sorting/filtering methods ##
    def sort_examples_by_verdicts(self, key: Tuple[ExampleVerdict, ...], reverse=True):
        """
        Sort the examples of this L1Doctest by the given key. The key is a tuple of `ExampleVerdict`.
        This method set the examples of this L1Doctest as the sorted examples.
        """
        sorted_example = sorted(self.get_examples(), key=lambda x: isinstance(x.get_verdict(), key), reverse=reverse)
        self.set_examples(sorted_example)
    
    def filter_examples_by_verdicts(self, key: Tuple[ExampleVerdict, ...]):
        """Filter the examples of this L1Doctest by the given key. The key is a tuple of `ExampleVerdict`.
        Return a list of examples that match the given key.
        """
        return [example for example in self.__examples if example.get_verdict().__class__ in key]
    
    ## Check methods ##
    def has_examples(self):
        """
        Returns:
            bool: Returns True if this `L1Doctest` contains at least one `Example`. 
            Otherwise, returns False.
        """
        return len(self.__examples) > 0
    
    def has_only_tests(self):
        """ 
        Return True if this L1Doctest contains only tests. Otherwise, returns False.
        """
        return self.count_tests() > 0 and self.count_tests() == len(self.__examples)
    
    def has_only_setUps(self):
        """
        Return True if this L1Doctest contains only setups. Otherwise, returns False.
        """
        return self.count_setups() > 0 and self.count_setups() == len(self.__examples)
    
    ## Add and remove methods ##
    def add_example(self, example:Example):
        """
        Add an example to the L1Doctest.

        Args:
            example (Example): The example to add.
        """
        self.__examples.append(example)
        
    def remove_example(self, example:Example):
        """
        Remove an example from the L1Doctest.

        Args:
            example (Example): The example to remove.
        """
        self.__examples.remove(example)
    
    # #################### ##
    ## Getters and Setters ##
    def get_filename(self):
        return self.__filename
    
    def get_node_lineno(self):
        """Return the line number of the node of the L1Doctest. 
        The node is the function or the class associated to the L1Doctest. """
        return self.__node_lineno
    
    def get_examples(self):
        return self.__examples
    
    def set_examples(self, examples:List[Example]):
        self.__examples = examples
    
    def get_name(self):
        """Return the name of the L1Doctest. The name is the name of the function or the class."""
        return self.__name
    
    def get_start_end_lineno(self) -> Tuple[int, int]:
        """Return the start and the end line number of the docstring of the L1Doctest."""
        return (self.__start_lineno, self.__end_lineno)

    def get_start_lineno(self):
        """Return the start line number of the docstring of the L1Doctest.""" 
        return self.__start_lineno
    
    def set_start_lineno(self, start_lineno):
        self.__start_lineno = start_lineno
    
    def get_end_lineno(self):
        """Return the end line number of the docstring of the L1Doctest."""
        return self.__end_lineno
    
    def set_end_lineno(self, end_lineno):
        self.__end_lineno = end_lineno
        
    def get_flag(self):
        """Return the flag of the L1Doctest. The flag is the global verdict of the L1Doctest."""
        return self.__flag


## The L1DocTestParser class 
class L1TestAstParser():
    """
    The L1DocTestParser is responsible for parsing the source and extracts the L1DocTests.
    The main method is `get_l1doctests()` which takes a list of AST nodes and returns a list of L1DocTest.
    
    Example of use:
        - You could parse the source by invoking the get_supported_nodes() method, then pass 
        the returned list of AST nodes to the get_l1doctests() method.
        
        >>> parser = L1TestAstParser("filename.py", "source")
        >>> list_nodes = parser.get_supported_nodes()
        >>> l1doctests = parser.get_l1doctests(list_nodes)
        
        - You could also get all the L1Doctests by invoking directly the get_l1doctests() method, without 
        parameters. In this case, the source will be firstly parsed then the L1Doctests will be extracted.
        
        >>> parser = L1TestAstParser("filename.py", "source")
        >>> l1doctests = parser.get_l1doctests()
    """
    def __init__(self, filename:str="", source:str="", mode="exec") -> None:
        self._source = source
        self._filename = filename
        self._mode = mode

    def get_l1doctests(self, list_nodes: List[ast.AST]=None) -> List[L1DocTest]:
        """
        Takes a list of supported nodes and returns a list of L1DocTest. 
        Each L1DocTest represents an AST node. 
        """
        list_nodes = list_nodes or self.get_supported_nodes()
        l1doctests: List[L1DocTest] = []
        doctest_parser = DocTestParser()        
        for node in list_nodes:
            if isinstance(node, SUPPORTED_TYPES):
                l1doctest = L1DocTest(self._filename, create_node_representation(node), node.lineno)
                if node.body:
                    first_stmt = node.body[0]
                    if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Str):
                        l1doctest.set_start_lineno(first_stmt.lineno)
                        l1doctest.set_end_lineno(first_stmt.end_lineno)
                
                docstring = ast.get_docstring(node, False) or ""
                parsed_doc = doctest_parser.parse(docstring, name=self._filename)

                l1doctest.set_examples(self.__filter_example_instances(l1doctest, parsed_doc))
                l1doctests.append(l1doctest)
        return l1doctests

    def get_l1doctest(self, node:ast.AST):
        """
        Returns the corresponding L1DocTest for the given node.
        
        Args: 
            node (ast) : the ast node.  
            This parameter cannot be None and should be a supported type. See `SUPPORTED_TYPES`.
        """
        assert node != None and isinstance(node, SUPPORTED_TYPES)
        return self.get_l1doctests([node])

    def get_supported_nodes(self):
        """
        Get only the nodes that can have a docstring. 
        The supported nodes are repported to ~SUPPORTED_TYPES~ constant.
        
        Returns:
            list[ast.AST]: returns only the nodes that can have a docstring. 
        
        Raises: 
            Error: A compilation error raised by the AST module.
        """
        source_nodes = [node for node in self.__get_ast_body() if isinstance(node, SUPPORTED_TYPES)]
        all_nodes = []
        # get all the supported nodes from a source content
        self.__recursive_walking(source_nodes, all_nodes)
        return all_nodes      
    
    def __filter_example_instances(self, l1_doctest:L1DocTest, parsed_doc:list) -> List[Example]:
        """
        The filter can return an empty list if there's no example 
        in the parsed docstring. Otherwise, it will return a list of the `Example` instances 
        matching the given l1doctest.
        """
        examples = []
        for test in parsed_doc:
            if isinstance(test, Example):
                test.lineno = test.lineno + l1_doctest.get_start_lineno() - 1
                examples.append(test)
        return examples
    
    def __get_ast_body(self):
        """
        Returns the body(list of nodes) of the root node of the AST tree.
        
        Raises: 
            Error: A compilation error raised by the AST module.
        """
        return ast.parse(self._source, self._filename, mode=self._mode).body
    
    def __recursive_walking(self, list_nodes:list, all_nodes:list):
        """
        Search all the supported nodes in the AST tree. Even sub-nodes are visited.
        This is a recursive function, so all the visited nodes are added in the ~all_nodes~
        parameter.
        """
        for node in list_nodes:
            if isinstance(node, SUPPORTED_TYPES):
                all_nodes.append(node)
                self.__recursive_walking(node.body, all_nodes)
            
    def get_filename(self):
        return self._filename
    
    def set_filename(self, filename: str):
        self._filename = filename
    
    def get_source(self):
        return self._source
    
    def set_source(self, source: str):
        self._source = source
        
    def get_mode(self):
        return self._mode
    
    def set_mode(self, mode):
        self._mode = mode
