from thonny.config_ui import ConfigurationPage
from ..properties import PLUGIN_NAME
from thonny import get_workbench

# Default config
DEFAULT_DOC_GENERATION_AFTER_RETURN = True
DEFAULT_IMPORT_MODULE_IN_SHELL = True
DEFAULT_OPEN_RED_TESTS = False
DEFAULT_HIGHLIGHT_EXCEPTIONS = False
DEFAULT_GLOBAL_VIEW = True
DEFAULT_EXCEPTION_DETAIL = False

# Option names
AUTO_GENERATON_DOC = "auto_generaton_doc"
IMPORT_MODULE = "import_module"
OPEN_RED_ROWS = "open_red_rows"
HIGHLIGHT_EXCEPTIONS = "highlight_exceptions"
GLOBAL_VIEW = "global_view"
EXCEPTION_DETAIL = "exception_detail"

# Dict of options name and default value
OPTIONS = {
    AUTO_GENERATON_DOC : DEFAULT_DOC_GENERATION_AFTER_RETURN,
    IMPORT_MODULE : DEFAULT_IMPORT_MODULE_IN_SHELL,
    OPEN_RED_ROWS : DEFAULT_OPEN_RED_TESTS,
    HIGHLIGHT_EXCEPTIONS: DEFAULT_HIGHLIGHT_EXCEPTIONS,
    GLOBAL_VIEW: DEFAULT_GLOBAL_VIEW,
    EXCEPTION_DETAIL: DEFAULT_EXCEPTION_DETAIL
}

def init_options():
    """
    Initialise dans le workbench les options du plugin.
    """
    for opt in OPTIONS :
        if not get_workbench().get_option(opt) :
            get_workbench().set_default("%s." % PLUGIN_NAME + opt, OPTIONS[opt])

def get_option(name: str): 
    """
    Renvoie la valeur dans le workbench de l'option passée en paramètre.

    Paramètres:
    - name : le nom de l'option, tel que définie ds globals.py 
    """
    return get_workbench().get_option("%s." % PLUGIN_NAME + name)

def set_option(name, value):
    get_workbench().set_option("%s." % PLUGIN_NAME + name, value)

class plugin_configuration_page(ConfigurationPage):
    def __init__(self, master):
        ConfigurationPage.__init__(self, master)
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, AUTO_GENERATON_DOC), 
                          "Générer la docstring automatiquement après un saut de ligne au niveau du nom d'une fonction.")
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, IMPORT_MODULE), 
                          "Importer le module exécuté dans le shell.")
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, GLOBAL_VIEW), 
                          "Fermer, initialement, toutes les lignes de la vue %s." % PLUGIN_NAME)
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, OPEN_RED_ROWS), 
                          "Ouvrir, initialement, les tests rouges dans la vue %s." % PLUGIN_NAME)
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, HIGHLIGHT_EXCEPTIONS), 
                          "Mettre en évidence les tests en échec (seulement ceux qui lèvent une exception).")