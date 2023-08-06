from typing import List
import re
from thonny import get_workbench
from functools import partial
from ..properties import PLUGIN_NAME
import tkinter as tk
from ..utils import  get_photoImage 
from thonnycontrib import l1test_frontend 

_OUTLINE_REGEX = r"\s*(?P<type>def|class)[ ]+(?P<name>[\w]+)"

class OutlinedNode():
    def __init__(self, type:str, name:str, lineno:int) -> None:
        self.__type = type
        self.__name = name
        self.__lineno = lineno
        self.icon = "outline_class.png" if self.__type == "class" else "outline_method.gif"
        
        self.__image = get_photoImage(self.icon)
    
    def get_type(self):
        return self.__type  
    
    def get_name(self):
        return self.__name  
    
    def get_lineno(self):
        return self.__lineno  
    
    def get_image(self):
        return self.__image    

class Outliner():   
    def __init__(self, workbench=get_workbench()) -> None:
        super().__init__()
        l1test_frontend._outliner = self
        
        workbench._init_menu()
        self.menu = tk.Menu(workbench.get_menu(PLUGIN_NAME), name="outliner_menu") 
        get_workbench().bind("<Button-1>", self.update_menu, True)
     
    def __parse(self, source:str) -> List[OutlinedNode]:
        """
        Parses a source and returns a list of the outlined nodes. 
        The outlined nodes are either a class or a function. For 
        each outlined node an object of type `OutlinedNode` is built 
        in which we store the type (class/function), the name and the lineno
        of the outlined node.
        """
        outlines = []
        lineno = 0
        for line in source.split("\n"):
            lineno += 1
            match = re.match(_OUTLINE_REGEX, line) 
            if match:
                outlined = OutlinedNode(match.group("type"), match.group("name"), lineno)
                outlines.append(outlined)
        return outlines
    
    def from_source_post_menu(self, source):
        self.menu.delete(0, tk.END)
        outlines = self.__parse(source)
        for outline in outlines: 
            label = "%s %s" % (outline.get_type(), outline.get_name())
            image = outline.get_image()
            self.menu.add_command(label=label, 
                                  image=image,
                                  command=partial(run_outlined_test, outline.get_lineno()),
                                  activebackground="white",
                                  activeforeground="darkblue",
                                  compound=tk.LEFT)
            # should save a reference to the image otherwise it will be garbage collected
            setattr(self, image.name, image)  

    def update_menu(self, event):
        if isinstance(event.widget, str) and "menu" in event.widget:
            editor = get_workbench().get_editor_notebook().get_current_editor()
            if editor is None:
                return
            source = editor.get_code_view().get_content()
            self.from_source_post_menu(source)
    
    def get_menu(self):
        return self.menu

def run_outlined_test(lineno:int):
    """
    Cette fonction est invoquée quand le button `Run test for selected function`
    suite à un clique droit sur une ligne du fichier.
    Cette fonction permet d'envoyer au l1test_backend la commande L1test avec en argument
    is_selected=True.
    """
    from thonnycontrib.l1test_frontend import get_l1test_runner
    get_l1test_runner().run_l1test(selected_line=lineno)


