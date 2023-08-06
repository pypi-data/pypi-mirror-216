import re
import sys
import textwrap
from ..backend.ast_parser import L1TestAstParser
from .doc_template import *
from thonny.tktextext import *  
from ..exceptions import DocGeneratorParserException, NoFunctionSelectedToDocumentException
from ..utils import replace_error_line, get_last_exception
from thonny.editors import EditorCodeViewText
from ..ThonnyLogsGenerator import log_doc_in_thonny

r""" Docstring Generator Module
Description:
------------
This module generates a docstring using the templates.

For a selected line the `DocGenerator` tries to verify if the selected line
corresponds to a function signature. If the selected line is a function 
signature so a the `DocGenerator` will build a custom function with the given
selected line and then it parses(with AST parser) this function. If the AST parser
fails so the error will be displayed in the ErrorView. otherwise, the docstring
will be generated.

About templates, the docstring generator invokes the `DefaultDocTemplate` by default. 
The `DocTemplate.DefaultDocTemplate` class contains an implementation 
of a default template. 

How to use the Generator in thonny IDE:
---------------------------------------
- Right click on a function or a class declaration(it's prototype) and choose 
in the `edit menu` ~Generate Docstring~ button. You can also select the short cut 
Alt+d after putting the cursor on the function(or a class) declaration.

- Just a return on a function declaration will generate its docstring.
"""

class DocParser:
    def __init__(self, filename="", source="", ast_parser:L1TestAstParser=None):
        self._filename = filename
        self._source = source
        self._ast_parser = L1TestAstParser(self._filename, self._source, mode="single") \
                            if not ast_parser else ast_parser
    
    def parse_source(self, error_line:int=None):
        """
        Parses the given `source` and returns a list of 
        AST nodes that may contains a doctsring.
        
        As the AST python module stated in its documentation, the AST nodes that can 
        contain a dosctring are reported at ~SourceParser.SUPPORTED_TYPES~.
        
        Args:
            error_line(int): Set it only if you want to change the error line in 
            the raised exception. If `None`, so the error line mentioned in the error will 
            be kept. 
        
        Raises:
            DocGeneratorParserException: if the ast parser is failed.
        """
        try :
            return self._ast_parser.get_supported_nodes()
        except Exception as e: # if a compilation error occurs during the parsing
            error_info = sys.exc_info()
            last_exception = get_last_exception(error_info)
            if error_line:
                last_exception = replace_error_line(last_exception, error_line)
            raise DocGeneratorParserException(last_exception)    
    
    def get_filename(self):
        return self._filename
    
    def set_filename(self, filename: str):
        self._filename = filename
        self._ast_parser.set_filename(filename)
    
    def set_source(self, source: str):
        self._source = source
        self._ast_parser.set_source(source)
        
    def get_source(self):
        return self._source 
    
    def set_ast_parser(self, parser) :
        self._ast_parser = parser
       
class DocGenerator(ABC):
    def __init__(self, parser=DocParser(), template:DocTemplate=None):
        self._parser = parser
        self._template = template
        
    def generate(self, signature:str, selected_lineno:int=None, text_widget:EditorCodeViewText=None) -> str:   
        """Generate a docstring from a given signature (or prototype).
        
        Args:
            - signature(str): The signature for which the docstring will be generated.
            The signature should always be finished by a ":" caractere, otherwise the 
            docstring not will be generated. 
            - selected_lineno(int, Optional): This parameter is optional. It is the line number
            of the signature. This will be usefull for errors raised by the AST parser.
            If the ast parser raises an exception, the line number of the exception will be set to
            the given lineno.
            - text_widget(EditorCodeViewText, Optional): The view in which the generated docstring will 
            be inserted. Set to `None` if you want just to get the generated docstring. If `None` the
            generated docstring will not be inserted in any widget.
        
        Return:
            str: returns the generated docstring.
        
        Raises:
            - NoFunctionSelectedToDocument: When a selected line don't corresponds to 
            a function declaration. 
            - DocGeneratorParserException: when the ast parser fails.
        """
        if signature is None: signature = ""
        
        # We should check that the line is a function declaration and that ends with ':' character. 
        declaration_match = re.match(r"\s*(?P<id>def|class)\s*.*\s*:\s*$", signature)

        if not declaration_match:
            raise NoFunctionSelectedToDocumentException("No signature is selected to document!\n")
        else:   
            id_signature = declaration_match.group("id") # c'est le tag <id> dans l'expression régulière
            
            self._template = DocTemplateFactory.create_template(id_signature) \
                                if not self._template else self._template
            
            generated_temp = self.__get_generated_template(signature, selected_lineno)
            
            indent = self.__compute_indent(signature)
            generated_doc = textwrap.indent(generated_temp, indent)
            if text_widget:
                # c'est içi que la docstring est ajoutée à l'éditeur
                text_widget.insert(str(selected_lineno + 1) + ".0", generated_doc)
            return generated_doc
            
    def __get_generated_template(self, signature:str, selected_lineno:int) -> str:
        """
        Creates a custom function with the given `signature` then parses this function and if the
        AST parser success so the docstring will be generated. If the AST parser fails, so the 
        reported exception will be raised.

        Args:
            signature (str): the signature for which the docstring will be generated.
            selected_lineno (int): the line that corresponds to the selected line. This arg is used 
            to change the error line in the reported exception to the given `selected_line`. Remember
            that the error line will be always "1" if the ast parser fails, because the parsed source
            contains only the custom function.
            
        Returns:
            (str): The generated template.
            
        Raises: 
            DocGeneratorParserException: when the ast parser fails.
        """
        # The approach is to take the signature of the selected function then
        # adds a custom body to this function.
        custom_func = self._create_custom_body(signature)
        
        # don't forgot that the result of parsing is a list of supported nodes
        # -> see the doc
        self._parser.set_source(custom_func)
        node = self._parser.parse_source(selected_lineno)[0] 
        
        # Generate an event in Thonny with l1test/ThonnyLogsGenerator.log_doc_in_thonny
        log_doc_in_thonny(node)
        
        return self._template.get_template(node)

    def __compute_indent(self, signature:str) -> int:
        """
        Get the indentation based on the whitespaces located in the given `signature`.

        Args:
            signature (str): a signature of a function

        Returns:
            int: returns the indentation based on the whitespaces located in the given `signature`.
        """
        space_match = re.search("^(\s+)", signature)
        python_indent = 4
        sig_indent = len(space_match.group(1)) if space_match else 0
        return " " * (sig_indent + python_indent)

    def _create_custom_body(self, signature:str):
        signature = signature.strip()
        indent = " " * 4
        return  signature + "\n" + indent + "pass"    
    
    def set_parser(self, parser: DocParser):
        self._parser = parser
        
    def get_parser(self):
        return self._parser
        
    def set_template(self, template: DocTemplate):
        self._template = template
    
    def get_template(self):
        return self._template
        
    def set_filename(self, filename: str):
        self._parser.set_filename(filename)