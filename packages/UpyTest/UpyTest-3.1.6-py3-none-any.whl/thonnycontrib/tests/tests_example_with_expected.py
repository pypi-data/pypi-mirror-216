from types import ModuleType
from thonnycontrib.backend.doctest_parser import ExampleWithExpected
from thonnycontrib.backend.evaluator import Evaluator
from thonnycontrib.exceptions import *
from thonnycontrib.backend.verdicts.EmptyTest import EmptyTest
from backend.verdicts.ExceptionVerdict import ExceptionVerdict
from backend.verdicts.FailedVerdict import FailedVerdict
from backend.verdicts.PassedVerdict import PassedVerdict
from thonnycontrib.backend.doctest_parser import *
import unittest as ut
from thonnycontrib.tests.backend_mock import *

# ########################################################
#    Tous les tests qui suivent utilisent l'invite `$$$`
#               AVEC une valeur attendue  
# ########################################################
class TestEvaluator(ut.TestCase):
    def setUp(self):
        self.evaluator = Evaluator(filename="<string>")
        self.mock_backend = backend_patch.start()
    
    def tearDown(self) -> None:
        del self.evaluator
        backend_patch.stop()
    
    def test_evaluate_when_empty_verdict(self):
        """
        Ce test vérifie:
        1. Quand il n'y a aucun test dans une docstring alors aucun 
        type Example n'est produit. On assure plutôt que la liste
        d'Example associée au noeud est vide.
        2. Lorsqu'un noeud ast ne contient aucun test alors un
        verdict de type `EmptyTest` est renvoyé.
        """
        
        fake_source = \
"""
def f(a, b):
    if a < 0 and b < 0:
        return None
    return a + b
"""
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        l1doctests = self.evaluator.get_test_finder().extract_examples()
        
        # on assure qu'il existe un seul noeud AST
        self.assertTrue(len(l1doctests) == 1)
        for l1doctest in l1doctests:
            # on assure que le noeud AST ne contient aucun type Example
            self.assertEqual(l1doctest.get_examples(), []) 
        
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
            
    def test_evaluate_when_passed_verdict(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Le verdict renvoyé est de type `PassedTest`. 
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(1, 2)
    3
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_type(ExampleWithExpected)
        
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
    
    def test_evaluate_when_failed_verdict(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Le verdict renvoyé est de type `FailedTest`. 
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(1, 2)
    2
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_type(ExampleWithExpected)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on assure qu'il existe un seul noeud AST avec ses verdicts
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 1) 
            # on assure que le verdict est bien du type `FailedTest`
            self.assertTrue(isinstance(verdicts[0], FailedVerdict))
            self.assertTrue('Expected: 2, Got: 3' in verdicts[0].get_detail_failure())
    
    def test_evaluate_when_exception_verdict(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Le verdict renvoyé est de type `ExceptionTest` car la 
        comparaison `if a < 0 and b < 0:` va échouer si l'argument `a` ou `b`
        ne sont pas de type `int`.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f('j', 2)
    2
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_type(ExampleWithExpected)
        
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
            # on assure que le message d'exception inclu l'erreur `TypeError`
            self.assertTrue("TypeError: '<' not supported between instances of 'str' and 'int'" \
                                in verdicts[0].get_detail_failure())
    
    def test_evaluate_when_expected_is_none(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Quand la valeur attendue est None et que la fonction executée renvoie None
        alors on aura un verdict de type `PassedTest`
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(-1, -1)
    None
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_type(ExampleWithExpected)
        
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
    
    def test_evaluate_when_syntax_error(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Quand il y a une erreur de syntax au niveau du test alors
        un verdict `ExceptionTest` est renvoyé
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(1, 1
    2
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_type(ExampleWithExpected)
        
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
            # on assure que le verdict inclu l'erreur de syntaxe dans son message
            self.assertTrue(SyntaxError.__name__ in verdicts[0].get_detail_failure())
    
    def test_evaluate_when_runtime_error(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Quand la fonction executée utilise une variable non déclarée alors
        on assure que le verdict est de type `ExceptionTest`
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(1, 1)
    2
    '''
    if a < 0 and b < 0:
        return None
    return a + b * c
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_type(ExampleWithExpected)
        
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
            # on assure que le verdict inclu l'erreur NameError dans son message
            self.assertTrue(NameError.__name__ in verdicts[0].get_detail_failure()) 
            # on assure que le détail de l'erreur est inclue dans le message du verdict 
            self.assertTrue("name 'c' is not defined" in verdicts[0].get_detail_failure())  
            
    def test_evaluate_when_an_exception_is_expected_and_raised(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Quand la valeur attendue est une exception et que la fonction lève 
        une exception alors on aura le verdict `ExceptionTest`.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(-1, -1)
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
        self._assert_example_type(ExampleWithExpected)
        
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
            # on assure que le verdict inclu l'exception Exception dans son message
            self.assertTrue(Exception.__name__ in verdicts[0].get_detail_failure()) 
            # on assure que le message de l'Exception est inclue dans le message du verdict 
            self.assertTrue("a et b doivent être positifs" in verdicts[0].get_detail_failure()) 
            
    def test_evaluate_when_an_exception_is_expected_but_not_raised(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithExpected` est le type `Example` extrait 
        par le doctest parser.
        2. Quand la valeur attendue est une exception mais la fonction ne lève pas
        une exception, dans ce cas on aura le verdict `FailedTest`.
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(-1, -1)
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
        self._assert_example_type(ExampleWithExpected)
        
        # ###################################################
        # ------------- Vérification du verdict -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on assure qu'il existe un seul noeud AST avec ses verdicts
        self.assertTrue(len(node_verdicts) == 1)
        for node, verdicts in node_verdicts.items():
            # on assure qu'il existe bien un seul verdict
            self.assertTrue(len(verdicts) == 1) 
            # on assure que le verdict est bien du type `FailedTest`
            self.assertTrue(isinstance(verdicts[0], FailedVerdict))
            self.assertTrue('Expected: Exception, Got: None' in verdicts[0].get_detail_failure())
    
    def test_evaluate_when_setup(self):
        """
        Ce test vérifie:
        1. Le type `ExampleWithoutExpected` est le type `Example` extrait 
        par le doctest parser.
        2. si un test est setup mais il existe quand même une valeur attendue
        alors le verdict renvoyée est de type `ExceptionTest`
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$ a = 0
    0
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # ###########################################################
        # ------------- Vérification du type Example ----------------
        self._assert_example_type(ExampleWithExpected)
        
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
            # on assure que le détail de l'erreur est inclue dans le message du verdict 
            self.assertTrue("invalid syntax. Maybe you meant '==' or ':=' instead of '='?" \
                            in verdicts[0].get_detail_failure()) 
    
    
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
        
