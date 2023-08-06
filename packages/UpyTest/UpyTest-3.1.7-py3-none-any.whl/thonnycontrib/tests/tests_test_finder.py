from ast import AST
import unittest as ut

from thonnycontrib.backend.evaluator import L1TestFinder
from thonnycontrib.backend.doctest_parser import (
    ExampleWithoutExpected, 
    ExampleExceptionExpected, 
    ExampleWithExpected
)
from thonnycontrib.exceptions import *
from thonnycontrib.backend.doctest_parser import *

# ########################################################
#  Tous les tests qui suivent testent le phase du parsing 
# ########################################################
class TestTestFinder(ut.TestCase):
    def setUp(self):
        self.test_finder = L1TestFinder(filename="<string>")
    
    def test_doctest_parser_when_no_examples(self):
        """
            Ce test vérifie que s'il n'y a aucun test dans le noeud ast
            alors aucun type `Example` n'est renvoyé mais plutôt une liste vide.
        """
        fake_source = \
"""
def f(a, b):
    if a < 0 and b < 0:
        return None
    return a + b
"""
        
        self.test_finder.set_source(fake_source)
        l1doctests = self.test_finder.extract_examples()

        # on assure qu'il existe un seul noeud AST
        self.assertTrue(len(l1doctests) == 1)
        for l1doctest in l1doctests:
            # on assure que le noeud AST ne contient aucun type Example
            self.assertEqual(l1doctest.get_examples(), []) 
    
        
    def test_doctest_parser_when_ExampleWithoutExpected(self):
        """
            Ce test vérifie que si l'invite est `$$$` et qu'il n'existe pas
            un `want` alors on aura le type `ExampleWithoutExpected`.
        """
        fake_source = \
"""
def f(a, b):
    '''
    $$$ a=0
    
    '''
    if a < 0 and b < 0:
        return None
    return a + b
"""
        self.test_finder.set_source(fake_source)
        l1doctests = self.test_finder.extract_examples()
        
        # on assure qu'il existe un seul noeud ast
        self.assertTrue(len(l1doctests) == 1)
        
        for l1doctest in l1doctests:
            examples = l1doctest.get_examples()
            self.assertTrue(len(examples) == 1) # on assure qu'il existe un seul type Example 
            self.assertTrue(isinstance(examples[0], ExampleWithoutExpected))
    
    
    def test_doctest_parser_when_ExampleWithExpected(self):
        """
            Ce test vérifie que si l'invite est `$$$` et qu'il existe
            un `want` alors on aura le type `ExampleWithExpected`.
        """
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(2, 3)
    5
    '''
    if a < 0 and b < 0:
        return None
    return a + b
"""
        self.test_finder.set_source(fake_source)
        l1doctests = self.test_finder.extract_examples()
        
        # on assure qu'il existe un seul noeud ast
        self.assertTrue(len(l1doctests) == 1)
        
        for l1doctest in l1doctests:
            examples = l1doctest.get_examples()
            self.assertTrue(len(examples) == 1) # on assure qu'il existe un seul type Example 
            self.assertTrue(isinstance(examples[0], ExampleWithExpected))
     
            
    def test_doctest_parser_when_ExampleExceptionExpected(self):
        """
            Ce test vérifie que si l'invite est `$$e` alors on aura 
            le type `ExampleExceptionExpected`.
        """
        fake_source = \
"""
def f(a, b):
    '''
    $$e f(2, 3)
    Exception
    '''
    if a < 0 and b < 0:
        raise Exception("a et b doivent être positifs")
    return a + b
"""
        self.test_finder.set_source(fake_source)
        l1doctests = self.test_finder.extract_examples()
        
        # on assure qu'il existe un seul noeud ast
        self.assertTrue(len(l1doctests) == 1)
        
        for l1doctest in l1doctests:
            examples = l1doctest.get_examples()
            self.assertTrue(len(examples) == 1) # on assure qu'il existe un seul type Example 
            self.assertTrue(isinstance(examples[0], ExampleExceptionExpected))
    
    
    def test_doctest_parser_when_unauthorized_exception(self):
        """
            Ce test vérifie que si une exception est attendue alors que
            l'invite de commande n'est pas un `$$e`, on aura pas alors le type 
            `ExampleExceptionExpected`.
        """
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(-2, -3)
    Exception
    '''
    if a < 0 and b < 0:
        raise Exception("a et b doivent être positifs")
    return a + b
"""
        self.test_finder.set_source(fake_source)
        l1doctests = self.test_finder.extract_examples()
        
        # on assure qu'il existe un seul noeud ast
        self.assertTrue(len(l1doctests) == 1)
        
        for l1doctest in l1doctests:
            examples = l1doctest.get_examples()
            self.assertTrue(len(examples) == 1) # on assure qu'il existe un seul type Example 
            # on assure que ce n'est pas un type `ExampleExceptionExpected`
            self.assertTrue(not isinstance(examples[0], ExampleExceptionExpected))
            # mais que c'est un type `ExampleWithExpected`
            self.assertTrue(isinstance(examples[0], ExampleWithExpected))

    def test_evaluate_when_a_space_is_missing_after_prompt_case_1(self):
        """
        Ce test vérifie:
            1. Quand il manque un espace après l'invite `$$$` alors 
               une exception de type `SpaceMissingAfterPromptException` est levée
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$$f(1, 1)
    2
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.test_finder.set_source(fake_source)
        with self.assertRaises(SpaceMissingAfterPromptException):
            self.test_finder.extract_examples()
            
    def test_evaluate_when_a_space_is_missing_after_prompt_case_2(self):
        """
        Ce test vérifie:
            1. Quand il manque un espace après l'invite `$$e` alors 
               une exception de type `SpaceMissingAfterPromptException` est levée
        """
        
        fake_source = \
"""
def f(a, b):
    '''
    $$ef(1, 1)
    2
    '''
    if a < 0 and b < 0:
        return None
    return a + b
""" 
        
        self.test_finder.set_source(fake_source)
        with self.assertRaises(SpaceMissingAfterPromptException):
            self.test_finder.extract_examples()

if __name__ == '__main__':
    ut.main()   