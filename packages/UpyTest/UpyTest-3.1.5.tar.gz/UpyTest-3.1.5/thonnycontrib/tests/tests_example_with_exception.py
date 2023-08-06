import ast
from types import ModuleType
from thonnycontrib.backend.doctest_parser import ExampleExceptionExpected
from thonnycontrib.backend.evaluator import Evaluator
from thonnycontrib.exceptions import *
from thonnycontrib.backend.verdicts.EmptyTest import EmptyTest
from backend.verdicts.ExceptionVerdict import ExceptionVerdict
from backend.verdicts.FailedVerdict import FailedVerdict
from backend.verdicts.PassedVerdict import PassedVerdict
from backend.verdicts.FailedWhenExceptionExpectedVerdict import FailedWhenExceptionExpectedVerdict
from thonnycontrib.tests.backend_mock import *

from thonnycontrib.backend.doctest_parser import *
import unittest as ut

# ########################################################
#    Tous les tests qui suivent utilisent l'invite `$$e`
# ########################################################
class TestEvaluator(ut.TestCase):
    def setUp(self):
        self.evaluator = Evaluator(filename="<string>")
        self.mock_backend = backend_patch.start()
        
    def tearDown(self) -> None:
        del self.evaluator   
        backend_patch.stop()
    
    def test_evaluate_when_exception_expected_and_is_raised(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Si une exception est attendue et que la fonction executée lève 
        cette exception alors on aura un `PassedTest`.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$e f(-1, -2)
    Exception
    '''
    if a < 0 and b < 0:
        raise Exception("a et b doivent être positifs")
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_types(ExampleExceptionExpected)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on assure qu'il existe un seul noeud AST avec ses verdicts
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 1) 
            # on assure que le verdict est bien du type `PassedTest`
            self.assertTrue(isinstance(verdicts[0], PassedVerdict))
           
    def test_evaluate_when_exception_expected_but_not_raised(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Si une exception est attendue et que la fonction executée ne lève pas
        cette exception alors on aura un `FailedWhenExceptionExpectedTest`.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$e f(-1, -2)
    Exception
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_types(ExampleExceptionExpected)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on assure qu'il existe un seul noeud AST avec ses verdicts
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 1) 
            # on assure que le verdict est bien du type `FailedWhenExceptionExpectedTest`
            self.assertTrue(isinstance(verdicts[0], FailedWhenExceptionExpectedVerdict))
            self.assertTrue("Exception was not raised by f(-1, -2)" in verdicts[0].get_detail_failure())
            
    def test_evaluate_when_exception_expected_but_dont_inherit_from_base_exception(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Si l'exception attendue n'hérite pas(directement ou indirectement) de 
        la classe `BaseException` alors un verdict de type `ExceptionTest` 
        est renvoyé.
        """
        
        fake_source = \
"""
class MyException(): pass

def f(a, b):
    '''
    $$e f(-1, -2)
    MyException
    '''
    if a < 0 and b < 0:
        raise MyException()
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        # on assure qu'il existe deux noeud AST(la classe MyException() et la fonction)
        l1doctests = self.evaluator.get_test_finder().extract_examples()
        self.assertTrue(len(l1doctests) == 2)
        for l1doctest in l1doctests:
            if isinstance(l1doctest.get_node(), ast.FunctionDef):
                examples = l1doctest.get_examples()
                self.assertTrue(len(examples) == 1) # on assure qu'il existe un seul type Example 
                self.assertTrue(isinstance(examples[0], ExampleExceptionExpected))
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on assure qu'il existe deux noeuds AST 
        self.assertTrue(len(node_verdicts) == 2)
        for node, verdicts in node_verdicts.items():
            if isinstance(node, ast.FunctionDef):
                # on assure qu'il existe bien un seul verdict
                self.assertTrue(len(verdicts) == 1) 
                # on assure que le verdict est bien du type `ExceptionTest`
                self.assertTrue(isinstance(verdicts[0], ExceptionVerdict))
                self.assertTrue(TypeError.__name__ in verdicts[0].get_detail_failure())
                self.assertTrue("is not a class of type exception." in verdicts[0].get_detail_failure())
    
    def test_evaluate_when_exception_expected_but_is_not_declared(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Si l'exception attendue n'est pas retrouvée(n'est jamais déclarée)
        alors le verdict `ExceptionTest` est renvoyé.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$e f(-1, -2)
    UnknownException
    '''
    if a < 0 and b < 0:
        raise Exception()
    return a + b
""" 
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        # on assure qu'il existe seul noeud AST
        self._assert_example_types(ExampleExceptionExpected)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on assure qu'il existe un seul noeud AST 
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 1) 
            # on assure que le verdict est bien du type `ExceptionTest`
            self.assertTrue(isinstance(verdicts[0], ExceptionVerdict))
            self.assertTrue(NameError.__name__ in verdicts[0].get_detail_failure())
            self.assertTrue("The expected exception `UnknownException` cannot be found." \
                                in verdicts[0].get_detail_failure())
            
    def test_evaluate_when_exception_expected_but_an_other_exception_is_raised(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Si l'exception attendue n'est pas levée par la fonction executée
        alors le verdict `FailedWhenExceptionExpectedTest` est renvoyé.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$e f(-1, -2)
    Exception
    '''
    if a < 0 and b < 0:
        raise ValueError()
    return a + b
""" 
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        # on assure qu'il existe seul noeud AST
        self._assert_example_types(ExampleExceptionExpected)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on assure qu'il existe un seul noeud AST 
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 1) 
            # on assure que le verdict est bien du type `FailedWhenExceptionExpectedTest`
            self.assertTrue(isinstance(verdicts[0], FailedWhenExceptionExpectedVerdict))
            self.assertTrue("Exception was not raised by f(-1, -2)\nInstead, it raises :" \
                                in verdicts[0].get_detail_failure())
            self.assertTrue(ValueError.__name__ in verdicts[0].get_detail_failure())
           
    def test_evaluate_when_syntax_error(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Si le test contient une syntaxe erreur alors un verdict `ExceptionTest` 
        est renvoyé.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$e f(-1, -2
    Exception
    '''
    if a < 0 and b < 0:
        raise ValueError()
    return a + b
""" 
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        # on assure qu'il existe seul noeud AST
        self._assert_example_types(ExampleExceptionExpected)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on assure qu'il existe un seul noeud AST 
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 1) 
            # on assure que le verdict est bien du type `ExceptionTest`
            self.assertTrue(isinstance(verdicts[0], ExceptionVerdict))
            self.assertTrue(SyntaxError.__name__ in verdicts[0].get_detail_failure())
             
    def test_evaluate_when_exception_is_blank_or_empty(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Si l'exception attendue n'est pas retrouvée(n'est jamais déclarée)
        alors le verdict `ExceptionTest` est renvoyé.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$e f(-1, -2)   # Example of an empty <want> 
    $$e f(-1, -2)   # Example of a blank <want>
    
    '''
    if a < 0 and b < 0:
        raise Exception()
    return a + b
""" 
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_types(ExampleExceptionExpected, 2)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on assure qu'il existe un seul noeud AST 
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 2) 
            # on assure que le verdict est bien du type `ExceptionTest`
            self.assertTrue(isinstance(verdicts[0], ExceptionVerdict))
            self.assertTrue(ValueError.__name__ in verdicts[0].get_detail_failure())
            self.assertTrue("The expected exception cannot be empty or blank" \
                                in verdicts[0].get_detail_failure())
    
    
    def _assert_example_types(self, example_type: Example, len_examples=1):
        """
            Assert that the expected `Example` type is of type the given `example_type`.
            Also assert the number of the retrieved examples by given the `len_examples`
            parameter.
        """
        l1doctests = self.evaluator.get_test_finder().extract_examples()
        
        # on assure qu'il existe un seul noeud AST
        self.assertTrue(len(l1doctests) == 1)
        for l1_docTest in l1doctests:
            examples = l1_docTest.get_examples()
            self.assertTrue(len(examples) == len_examples) # on assure qu'il existe un seul type Example 
            for i in range(len_examples):
                self.assertTrue(isinstance(examples[i], example_type))
    
    def __build_module_from_source(self, source: str) -> ModuleType:
        """
        Build a module containing the functions declared in the given `source`.
        """
        from types import ModuleType
        fake_module = ModuleType(self.evaluator.get_filename())
        exec(source, fake_module.__dict__)
        return fake_module


if __name__ == '__main__':
    ut.main()   
        