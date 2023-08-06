from types import ModuleType
import unittest as ut
from thonnycontrib.l1test_frontend.l1test_treeview import L1TestTreeView
from thonnycontrib.backend.evaluator import Evaluator
from thonnycontrib.exceptions import *
from backend.verdicts.FailedWhenExceptionExpectedVerdict import FailedWhenExceptionExpectedVerdict
from thonnycontrib.backend.verdicts.EmptyTest import EmptyTest
from backend.verdicts.ExceptionVerdict import ExceptionVerdict
from backend.verdicts.FailedVerdict import FailedVerdict
from backend.verdicts.PassedVerdict import PassedVerdict
from thonnycontrib.backend.doctest_parser import *
from unittest.mock import *
from thonnycontrib.tests.backend_mock import *

# #######################################################
#    Tous les tests qui suivent vérifient le rendu ur la treeview
# #######################################################
class MockL1TestTreeView(L1TestTreeView):
    def __init__(self):
        pass
        
class TestTestReporter(ut.TestCase):
    def setUp(self):
        self.l1TestTreeview = MockL1TestTreeView()
        self.evaluator = Evaluator(filename="<string>")
        self.mock_backend = backend_patch.start()
    
    def tearDown(self) -> None:
        del self.evaluator
        backend_patch.stop()
    
    def test_summarize_case_1(self):
        fake_source = \
"""
def f(a, b):
    '''
    $$$ f(1, 1)     # Passed verdict
    2
    $$$ f(1, 1)     # Failed verdict
    0
    $$$ f(20, 20)   # Exception verdict
    0
    $$$ l = []      # It's a setup -> no verdict
    
    '''
    if a < 0 and b < 0:
        return None
    if a > 10 and b > 10:
        raise ValueError()
    return a + b
"""
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # #####################################################
        # ------------- Verification des verdicts -------------
        expected_verdicts_colors = {PassedVerdict: "green",
                                    FailedVerdict: "red",
                                    ExceptionVerdict: "red"}
        
        node_verdicts = self.evaluator.evaluate()
        
        
        # on s'assure qu'il existe un seul noeud AST 
        self.assertEqual(len(node_verdicts), 1)
        for node, verdicts in node_verdicts.items():
            # on s'assure que le nombre de verdicts calculés est exactement le nombre de verdicts attendus
            self.assertEqual(len(verdicts), len(expected_verdicts_colors.keys())) 
            # on assure que les verdicts récupérés sont exactement les verdicts attendus
            self.assertEqual([v.__class__ for v in verdicts], list(expected_verdicts_colors.keys()))

            # ##################################################################
            # ------------- Verification des couleurs des verdicts -------------
            self.assertEqual([v.get_tag() for v in verdicts], list(expected_verdicts_colors.values()))
        
        # ##################################################################
        # ------------------ Verification du SUMMARIZE ---------------------
        summarize = self.l1TestTreeview.build_summarize_object(node_verdicts)
        self.assertTrue(summarize.total == 3) 
        self.assertTrue(summarize.success == 1) 
        self.assertTrue(summarize.failures == 1) 
        self.assertTrue(summarize.errors == 1) 
        self.assertTrue(summarize.empty == 0)
    
    def test_summarize_case_2(self):
        """
        Dans ce test on vérifie le résultat de summarize quand la docstring 
        contient que des setups.
        """
        fake_source = \
"""
def f(a, b):
    '''
    $$$ a = 0
    
    '''
    return a + b
"""
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # #####################################################
        # ------------- Verification des verdicts -------------
        expected_verdicts_colors = {EmptyTest: "orange"}
        
        node_verdicts = self.evaluator.evaluate()
        
        # on s'assure qu'il existe un seul noeud AST 
        self.assertEqual(len(node_verdicts), 1)
        for node, verdicts in node_verdicts.items():
            # on s'assure que le nombre de verdicts calculés est exactement le nombre de verdicts attendus
            self.assertEqual(len(verdicts), len(expected_verdicts_colors.keys())) 
            # on assure que les verdicts récupérés sont exactement les verdicts attendus
            self.assertEqual([v.__class__ for v in verdicts], list(expected_verdicts_colors.keys()))

            # ##################################################################
            # ------------- Verification des couleurs des verdicts -------------
            self.assertEqual([v.get_tag() for v in verdicts], list(expected_verdicts_colors.values()))
        
        # ##################################################################
        # ------------------ Verification du SUMMARIZE ---------------------
        summarize = self.l1TestTreeview.build_summarize_object(node_verdicts)
        self.assertTrue(summarize.empty == 1)
        self.assertTrue(summarize.total == 0) 
        self.assertTrue(summarize.success == 0) 
        self.assertTrue(summarize.failures == 0) 
        self.assertTrue(summarize.errors == 0) 
            
    def test_summarize_case_3(self):
        """
        Dans ce test on vérifie le résultat de summarize quand la docstring 
        contient à la fois des setups et des tests.
        """
        fake_source = \
"""
def f(a, b):
    '''
    $$$ a = 1
    $$$ b = 1
    $$$ f(a, b)
    2
    '''
    return a + b
"""
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # #####################################################
        # ------------- Verification des verdicts -------------
        expected_verdicts_colors = {PassedVerdict: "green"}
        
        node_verdicts = self.evaluator.evaluate()
        
        # on s'assure qu'il existe un seul noeud AST 
        self.assertEqual(len(node_verdicts), 1)
        for node, verdicts in node_verdicts.items():
            # on s'assure que le nombre de verdicts calculés est exactement le nombre de verdicts attendus
            self.assertEqual(len(verdicts), len(expected_verdicts_colors.keys())) 
            # on assure que les verdicts récupérés sont exactement les verdicts attendus
            self.assertEqual([v.__class__ for v in verdicts], list(expected_verdicts_colors.keys()))

            # ##################################################################
            # ------------- Verification des couleurs des verdicts -------------
            self.assertEqual([v.get_tag() for v in verdicts], list(expected_verdicts_colors.values()))
        
        # ##################################################################
        # ------------------ Verification du SUMMARIZE ---------------------
        summarize = self.l1TestTreeview.build_summarize_object(node_verdicts)
        self.assertTrue(summarize.total == 1) 
        self.assertTrue(summarize.success == 1) 
        self.assertTrue(summarize.failures == 0) 
        self.assertTrue(summarize.errors == 0) 
        self.assertTrue(summarize.empty == 0)
        
    def test_summarize_case_4(self):
        """
        Dans ce test on vérifie le résultat de summarize quand 
        il existe 2 noeuds ast dont un d'eux contient que des setups 
        et l'autre contient des tests.
        """
        fake_source = \
"""
def minus(a, b):
    '''
    $$$ a = 1

    '''
    return a - b
    
def somme(a, b):
    '''
    $$$ a = 1
    $$$ b = 1
    $$$ somme(1, 1)
    2
    '''
    return a + b
"""
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # #####################################################
        # ------------- Verification des verdicts -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on s'assure qu'il existe deux noeuds AST 
        self.assertEqual(len(node_verdicts), 2)
        
        # on vérifie qu'il existe au total deux verdicts. Un pour la fonction `minus()`
        # et un autre pour la fonction `somme()`. 
        self.assertEqual(len(node_verdicts.values()), 2)
        
        # on vérifie le verdict de la fonction `minus()`
        minus_verdict = list(node_verdicts.values())[0]
        self.assertTrue(EmptyTest in [v.__class__ for v in minus_verdict])
        self.assertTrue("orange" in [v.get_tag() for v in minus_verdict])
        
        # on vérifie le verdict de la fonction `somme()`
        somme_verdict = list(node_verdicts.values())[1]
        self.assertTrue(PassedVerdict in [v.__class__ for v in somme_verdict])
        self.assertTrue("green" in [v.get_tag() for v in somme_verdict])
        
        # ##################################################################
        # ------------------ Verification du SUMMARIZE ---------------------
        summarize = self.l1TestTreeview.build_summarize_object(node_verdicts)
        self.assertTrue(summarize.total == 1) 
        self.assertTrue(summarize.success == 1) 
        self.assertTrue(summarize.failures == 0) 
        self.assertTrue(summarize.errors == 0) 
        self.assertTrue(summarize.empty == 1) 
    
    def test_summarize_case_5(self):
        """
        Dans ce test on vérifie le résultat de summarize quand 
        l'invite est `$$e`.
        """
        fake_source = \
"""
class NotAnException: pass

def somme(a, b):
    '''
    $$e somme(10, 10)       # le cas qui échoue(failed verdict)
    ValueError
    
    $$$ a, b = -1, -1
    $$e somme(a, b)         # le cas qui passe
    ValueError
    $$e somme(a, b)         
    UndefinedException      # le want déclare une exception qui n'existe pas
    $$e somme(a, b)
    Invalid name            # le want contient une erreur de nommage
    $$e somme(a, b)
    NotAnException          # le want n'est pas une exception qui hérite de BaseException
    '''
    if a > 9  or b > 9:
        raise Exception("a et b doivent être que des chiffres")
    if a < 0 and b < 0:
        raise ValueError()
    return a + b
"""
        self.evaluator.set_source(fake_source)
        self.evaluator.set_module(self.__build_module_from_source(fake_source))
        
        # #####################################################
        # ------------- Verification des verdicts -------------
        node_verdicts = self.evaluator.evaluate()
        
        # on s'assure qu'il existe deux noeuds AST : la fonction `somme()` et la classe `NotAnException`
        self.assertEqual(len(node_verdicts), 2)
        
        # on vérifie qu'il existe au total deux verdicts. Un pour la fonction `somme()`
        # et un autre pour la classe `NotAnException`. 
        self.assertEqual(len(node_verdicts.values()), 2)
        
        expected_verdicts = [FailedWhenExceptionExpectedVerdict, PassedVerdict] + \
                            [ExceptionVerdict]*3  # there are 3 exceptions verdicts
        expected_colors = ["red", "green"] + ["red"]*3
        
        # on vérifie le verdict de la fonction `somme()` qui est à la position 1.
        # La position 0 contient le verdict de la classe `NotAnException`
        somme_verdict = list(node_verdicts.values())[1]
        self.assertEqual(expected_verdicts, [v.__class__ for v in somme_verdict])
        self.assertEqual(expected_colors, [v.get_tag() for v in somme_verdict])
        
        # ##################################################################
        # ------------------ Verification du SUMMARIZE ---------------------
        summarize = self.l1TestTreeview.build_summarize_object(node_verdicts)  
        self.assertTrue(summarize.total == 5) 
        self.assertTrue(summarize.success == 1)  
        self.assertTrue(summarize.failures == 1) 
        self.assertTrue(summarize.errors == 3) 
        self.assertTrue(summarize.empty == 1)

             
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
        