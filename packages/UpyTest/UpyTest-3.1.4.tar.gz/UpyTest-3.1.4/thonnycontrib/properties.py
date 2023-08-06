PLUGIN_NAME = "L1Test"
DEBUG_NAME = "L1Test debugger"
ERROR_VIEW_LABEL = '%s errors' % PLUGIN_NAME

# ici vous pouvez changer la syntaxe du doctest. 
# version 2022 PJI : Actuellement on garde la syntaxe `$py`.
L1TEST_SYMBOL = "[$]py"
# version 2022 avant la rentrée
L1TEST_SYMBOL1 = "[$][$][$]"
L1TEST_SYMBOL2 = "[$]PY"
L1TEST_SYMBOL3 = "[$]py"
# L'invite des tests qui vérifient la levée d'exception
L1TEST_EXCEPTION_SYMBOL = "[$][$]e"


# ############################################################################################### #
#                       LES NOUVELLES VARIABLES VERSION 2023 PFE                                  #
# ############################################################################################### #

# Le nom de la commande magique pour l1test(doit toujours commencer par une majuscule)
BACKEND_COMMAND = "L1test"


# ############ Les noms des clés du dictionnaire renvoyé par le l1test_backend ############
# Le nom de l'attribut contenant les résulats des tests renvoyés par l1test_backend
VERDICTS = "verdicts"
# Le nom de l'attribut contenant une exception levée et renvoyée par l1test_backend
L1TEST_EXCEPTION = "l1test_exception"


# ############ Les labels des buttons du menu l1test treeview ############
UPDATE_FONT_LABEL = "Update the font"
PLACE_RED_TEST_ON_TOP_LABEL = "Place the red tests on the top"
SHOW_ONLY_RED_TESTS = "Show only red tests"
SHOW_ALL_TESTS = "Show all the tests"
RESUME_ORIGINAL_ORDER = "Resume original order"
GROUP_BY_VERDICTS = "Group by verdicts"
EXPAND_TEST_RESULTS = "Expand test results"
FOLD_TEST_RESULTS = "Fold test results"
REMOVE_ERROR_DETAILS = "Remove error details"
INCLUDE_ERROR_DETAILS = "Include error details"
CLEAR_LABEL = "Clear"
INCREASE_SPACE_BETWEEN_ROWS = "Inrease row height"
DECREASE_SPACE_BETWEEN_ROWS = "Decrease row height"

# Le message affiché sur la treeview quand `l1test` est en cours d'execution
L1TEST_IN_PROGRESS = "Executing tests in progress ..."

# the evaluation states
PENDING_STATE = "Pending" 
EXECUTED_STATE = "Executed" 
FINISHED_STATE = "Finished"

# The title of the error view when the docstring genertor shows the raised error
CANNOT_GENERATE_THE_DOCSTRING = "Cannot generate the docstring :"
# The title of the error view when the l1test shows the raised error
CANNOT_RUN_TESTS_MSG = "Cannot run %s :" %(PLUGIN_NAME)

# A special event that `L1TestTreeview` sends to ask `L1TestRunner` to shows the right view
L1TREE_VIEW_EVENT = "L1TreeviewEvent"