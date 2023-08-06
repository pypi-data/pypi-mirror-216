from types import ModuleType
import unittest as ut
from thonnycontrib.tests.backend_mock import *
from thonnycontrib.backend.doctest_parser import ExampleWithoutExpected
from unittest.mock import *
from thonnycontrib.backend.evaluator import Evaluator
from thonnycontrib.exceptions import *
from thonnycontrib.backend.verdicts.EmptyTest import EmptyTest
from backend.verdicts.ExceptionVerdict import ExceptionVerdict
from thonnycontrib.backend.doctest_parser import *

# #######################################################
#    Tous les tests qui suivent utilisent l'invite `$$$`
#               SANS valeur attendue  
# #######################################################
class TestEvaluator(ut.TestCase):
    def setUp(self):
        self.evaluator = Evaluator(filename="<string>")
        self.mock_backend = backend_patch.start()
    
    def tearDown(self) -> None:
        del self.evaluator
        backend_patch.stop()
    
    def test_evaluate_when_setup(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithoutExpected` est le type `Example` extrait 
        par le doctest parser.
        2. S'il existe que des setup dans un noeud AST alors le verdict renvoyé 
        est de type `EmptyTest`.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ a = 0
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_type(ExampleWithoutExpected)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
    
        # on assure qu'il existe un seul noeud AST avec ses verdicts
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 1) 
            # on assure que le verdict est bien du type `EmptyTest`
            self.assertTrue(isinstance(verdicts[0], EmptyTest))
    
    def test_evaluate_when_syntax_error_on_setup(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithoutExpected` est le type `Example` extrait 
        par le doctest parser.
        2. S'il existe une erreur de syntaxe au niveau du setup alors
        un verdict `ExceptionTest` sera renvoyé.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ a = 
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_type(ExampleWithoutExpected)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
    
        # on assure qu'il existe un seul noeud AST avec ses verdicts
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 1) 
            # on assure que le verdict est bien du type `ExceptionTest`
            self.assertTrue(isinstance(verdicts[0], ExceptionVerdict))
            self.assertTrue(SyntaxError.__name__ in verdicts[0].get_detail_failure()) 
    
    def _assert_example_type(self, example_type: Example):
        """Assert that the expected `Example` type is of type the given `example_type`"""
        l1doctests = self.evaluator.get_test_finder().extract_examples()
        
        # on assure qu'il existe un seul noeud AST
        self.assertTrue(len(l1doctests) == 1)
        for l1_docTest in l1doctests:
            examples = l1_docTest.get_examples()
            self.assertTrue(len(examples) == 1) # on assure qu'il existe un seul type Example 
            self.assertTrue(isinstance(examples[0], example_type))
    
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
        