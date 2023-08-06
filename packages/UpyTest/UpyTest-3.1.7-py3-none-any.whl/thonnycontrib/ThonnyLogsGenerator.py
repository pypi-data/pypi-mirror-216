'''
Permet de générer pour le plugin de log une synthèse des tests exécutés.
Corentin.
'''

from typing import List
from thonny import get_workbench
from .backend.ast_parser import L1DocTest

#Attention si le nom change ici, il faut aussi le changer dans Thonny-LoggingPlugin
NOM_EVENT_TEST = "l1Tests"
NOM_EVENT_DOC = "l1Tests.DocGenerator"
wb = get_workbench() 

def log_in_thonny(l1doctests: List[L1DocTest], selected):
    for l1doctest in l1doctests:
        for example in l1doctest.get_examples():
            wb.event_generate(NOM_EVENT_TEST, None, selected=selected, name=l1doctest.get_name(), **vars(example))

def log_doc_in_thonny(node):
    if wb:
        wb.event_generate(NOM_EVENT_DOC,None, name = node.name)
#La fonction anonyme car il faut une fonction pour bind, avec un argument parce qu'elle reçoit l'événement. 
if wb:   
    wb.bind(NOM_EVENT_TEST, lambda x : 0, True)
    wb.bind(NOM_EVENT_DOC, lambda x : 0, True)
