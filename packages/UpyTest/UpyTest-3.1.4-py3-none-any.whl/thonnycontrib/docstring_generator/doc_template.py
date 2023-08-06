from abc import *
import ast
from collections import namedtuple

# Un objet pour représenter le vocabulaire utilisé par le template 
class TemplateVocabulary:
    def __init__(self, todo_label="", summary_label="", param_label="",
                cu_label="", rtype_label="", rvalue_label="", test_label="", **kw) -> None:
        self.todo_label = todo_label
        self.summary_label = summary_label
        self.param_label = param_label,
        self.cu_label = cu_label,
        self.rtype_label = rtype_label,
        self.rvalue_label = rvalue_label,
        self.test_label = test_label
        
        # Le vocabulaire est flexible pour introduire d'autre mots
        for attribute, value in kw.items():
            setattr(self, attribute, value)
        
class DocTemplate(ABC):
    # Ces constantes peuvent être utilisées dans les classes d'implémention
    NEW_LINE = "\n"
    DOCSTRING_SYMBOL = '"""'
    
    def __init__(self, vocabulary=TemplateVocabulary()) -> None:
        vocabulary.todo_label = ""
        vocabulary.summary_label = "x_résumé_x"
        vocabulary.param_label = "Paramètres :"
        vocabulary.test_label = "Exemples :\n$$$ "
        vocabulary.cu_label = "Contraintes d'utilisation : "
        self.vocabulary = vocabulary
                            
    @abstractmethod
    def _format_general_summary(self) -> str:
        """
        Returns:
            str: Returns a label which will indicate to write a summary of the function.
        """
        pass
    
    @abstractmethod
    def _format_params(self, params) -> str:
        """
        Args:
            params (List): It's a list of the arguments.

        Returns:
            str: Returns the parameter representation section of a node in a docstring. 
        """
        pass
    
    @abstractmethod
    def _format_usage_constraints(self) -> str:
        """
        Returns:
            str: Returns the usage constraints representation section in a docstring.
        """
        pass
    
    @abstractmethod
    def _format_return_value(self) -> str:
        """
        Returns:
            str: Returns the return value representation section in a docstring.
        """
        pass
    
    @abstractmethod
    def _format_test_examples(self) -> str:
        """
        Returns:
            str: Returns the test examples representation section in a docstring.
        """
        pass
    
    @abstractmethod
    def get_template(self, node:ast.AST=None) -> str:
        """Build the complete docstring template. 
        This method must invoke the above abstract methods.
        
        Args:
            node (ast.AST): The AST node in which the dosctring will be generated.

        Returns:
            str: Returns the template representation. 
        """
        pass  
    
    @abstractmethod
    def get_id_signature(self) -> str: 
        pass      
    
class DocFunctionTemplate(DocTemplate):
    '''
    Modifié pour coller au cours d'Info L1
    '''
    def __init__(self) -> None:
        super().__init__()
        self.vocabulary.rvalue_label = "Valeur de retour "
        self.vocabulary.rtype_label = "(%s) :"
        
    def get_parameters(self, node:ast.AST):
        """
        Get the paramters of a given node.
        
        Args:
            node (ast.AST): An AST node. Must be an ast.FunctionDef or ast.AsyncFunctionDef

        Returns:
            List: Returns a List of arguments of the given node.
        """
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return node.args.args
        return []

    def _format_general_summary(self):
        return self.vocabulary.summary_label + self.NEW_LINE
    
    def _format_params(self, params):
        if params is None:
            return ""
        args_to_exclude = ["self", "cls"]
        label = self.vocabulary.param_label + self.NEW_LINE
        format_params = ""
        for p in params:
            arg_type = ast.unparse(p.annotation) if p.annotation else ""     
            arg_name = p.arg 
            if arg_name not in args_to_exclude: 
                format_params += "- %s (%s) : %s\n" %(arg_name, arg_type, self.vocabulary.todo_label)
        return label + format_params
    
    def _format_usage_constraints(self):
        return self.vocabulary.cu_label + self.vocabulary.todo_label + self.NEW_LINE   

    def _format_return_value(self, node: ast):
        #return_type = self.RETURN_TYPE_LABEL %(self.TODO_LABEL, self.NEW_LINE)
        return_type = ast.unparse(node.returns) if node.returns else ""
        return_descr = self.vocabulary.rtype_label % return_type + self.NEW_LINE
        return self.vocabulary.rvalue_label  + return_descr
    
    def _format_test_examples(self):
        label = self.vocabulary.test_label + self.NEW_LINE
        todo = self.vocabulary.todo_label + self.NEW_LINE
        return label + todo
        
    def get_template(self, node: ast.AST):
        return (
            self.DOCSTRING_SYMBOL + 
            self._format_general_summary() + self.NEW_LINE + 
            self._format_params(self.get_parameters(node))  + 
            self._format_return_value(node) + 
            self._format_usage_constraints() +
            self._format_test_examples() + 
            self.DOCSTRING_SYMBOL + self.NEW_LINE
        )
    
    def get_id_signature(self): 
        return "def" 

class DocClassTemplate(DocTemplate): 
    def _format_general_summary(self):
        return self.vocabulary.summary_label + self.NEW_LINE
    
    def _format_params(self):
        return self.vocabulary.param_label
     
    def _format_usage_constraints(self):
        return (self.vocabulary.cu_label +
                self.vocabulary.todo_label +
                self.NEW_LINE 
            )  

    def _format_return_value(self):
        return self.vocabulary.rvalue_label
    
    def _format_test_examples(self):
        label = self.vocabulary.test_label + self.NEW_LINE
        todo = self.vocabulary.todo_label + self.NEW_LINE
        return label + todo
            
    def get_template(self, node):
        return self.DOCSTRING_SYMBOL + \
               self._format_general_summary() + self.NEW_LINE + \
               self._format_usage_constraints() + \
               self._format_test_examples() + \
               self.DOCSTRING_SYMBOL + self.NEW_LINE

    def get_id_signature(self): 
        return "class" 

class DocTemplateFactory:            
    @staticmethod
    def create_template(type:str):
        return DocTemplateFactory.__search_type(type)
    
    @staticmethod
    def __docTemplate_subclasses(cls=DocTemplate):
        return set(cls.__subclasses__()) \
               .union([s for c in cls.__subclasses__() \
                            for s in DocTemplateFactory.__docTemplate_subclasses(c)])
    
    @staticmethod
    def __search_type(type:str) -> DocTemplate|None:
        template_types = DocTemplateFactory.__docTemplate_subclasses()
        
        find_type = [t() for t in template_types if type==t().get_id_signature()]
        return find_type[0] if find_type else None   
