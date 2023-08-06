from thonny import  tktextext, ui_utils
from thonny.ui_utils import scrollbar_style
from thonnycontrib.utils import get_font_size_option, get_font_family_option
from .l1test_error_view import L1TestErrorView
from ..properties import *
from ..backend.doctest_parser import Example
from ..backend.ast_parser import L1DocTest, L1DocTestFlag
from ..backend.verdicts.ExceptionVerdict import ExceptionVerdict
from ..backend.verdicts.FailedVerdict import FailedVerdict
from ..backend.verdicts.FailedWhenExceptionExpectedVerdict import FailedWhenExceptionExpectedVerdict
from ..utils import *
from functools import partial
from ..l1test_configuration.l1test_options import *
import tkinter as tk, tkinter.font as tk_font, thonny
from collections import namedtuple
from thonny.codeview import *
from typing import Dict, List
from copy import deepcopy

# La hauteur, par défault, d'une ligne dans une Treeview
ROW_HEIGHT = 40

SMALL_MARGIN = 1.1
NORMAL_MARGIN = 1.2

clickable_tag = "clickable"

# L'objet qui représente un summarize
Summarize = namedtuple('Summarize', ["total", "success", "failures", "errors", "empty"])

# Palette de couleurs utilisée par la treeview
COLORS:dict = { 'orange': '#e8770e',
                'red': 'red',
                'lightred': '#fcdbd9',
                'darkred': '#f7140c',
                'green': 'darkgreen',
                'blue': '#0000cc',
                'gray': 'gray'
            }

class L1TestTreeView(ttk.Frame):    
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, borderwidth=0, relief="flat")
        self.workbench = thonny.get_workbench()
        
        self._init_treeview()
        
        self._origin_l1doctests: List[L1DocTest] = dict()
        self._copy_l1doctests = self._origin_l1doctests.copy()
        
        # Le binding est censé augmenter/diminuer automatiquement la taille de la treeview
        self.workbench.bind("<Control-plus>", self.__observe_font_changing, True)
        self.workbench.bind("<Control-minus>", self.__observe_font_changing, True)
            
    def _init_treeview(self):
        """
        Creates the treeview widget.
        """
        self.vert_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, style=scrollbar_style("Vertical"))
        self.vert_scrollbar.grid(row=0, column=1, sticky=tk.NSEW, rowspan=3)
        
        self.init_header(row=0, column=0)
        
        spacer = ttk.Frame(self, height=1)
        spacer.grid(row=1, sticky="nsew")

        self.treeview = ttk.Treeview(self,yscrollcommand=self.vert_scrollbar.set)
        
        rows, columns = 2, 0
        self.treeview.grid(row=rows, column=columns, sticky=tk.NSEW)
        self.vert_scrollbar["command"] = self.treeview.yview
        self.columnconfigure(columns, weight=1)
        self.rowconfigure(rows, weight=1)
        
        # configure the only tree column
        self.treeview.column("#0", anchor=tk.W, stretch=tk.YES)
        
        # self.tree.heading('#0', text='Item (type @ line)', anchor=tk.W)
        self.treeview["show"] = ("tree",)

        for color_name, color in COLORS.items():
            if color_name == "lightred":
                self.treeview.tag_configure(color_name, background=color)
            else:
                self.treeview.tag_configure(color_name, foreground=color)
             
        self.treeview.tag_bind("clickable", "<<TreeviewSelect>>", self._on_select)
        self.treeview.tag_bind("nonClickable", "<<TreeviewSelect>>", self._remove_highlight_selection_effect)
        
        self.style = ttk.Style()
        self.style_mapping = self.style.map('Treeview')

        self.__update_tree_font(get_font_family_option(), get_font_size_option())

        # All the icons used in the treeview should be loaded here to keep thier references.
        # Otherwise, they will be garbage collected and the treeview will not show them.
        self.image_references = {}
        for flag in L1DocTestFlag:
            self.image_references[flag.name] = get_photoImage(flag.get_image())

        self.image_references["pending_icon.png"] = get_photoImage("pending_icon.png")
        self.image_references["error_icon.png"] = get_photoImage("error_icon.png")
        self.image_references["restart_icon.png"] = get_photoImage("restart_icon.png")
        
        # add a menu to the treeview
        self.menu = tk.Menu(self.treeview, name="menu", tearoff=False)
        
        # Here we handle the motion event of the treeview 
        self.treeview.bind("<Configure>", partial(self.__wrap_tree_content, self.treeview))
        self.treeview.bind("<Shift-I>", self.increase_row_height, True)
        self.treeview.bind("<Shift-D>", self.decrease_row_height, True)
        self.workbench.bind("<Shift-F>", self.update_font, True)

    # ------------------------------------
    # Fonctions pour le Header du treeview
    # ------------------------------------
    
    def init_header(self, row=0, column=0):
        """
        Initialize the header of the treeview. Initially, the header contains 
        only a `menu button` at the top right of the treeview. The options of the 
        menu are created by `post_button_menu()` method.

        Args:
            row (int): Always set to 0. Defaults to 0.
            column (int): Always set to 0. Defaults to 0.
        """
        header_frame = ttk.Frame(self, style="ViewToolbar.TFrame")
        header_frame.grid(row=row, column=column, sticky="nsew")
        header_frame.columnconfigure(0, weight=1)
        
        self.header_bar = tktextext.TweakableText(
            header_frame,
            borderwidth=0,
            relief="flat",
            height=1,
            wrap="word",
            padx=ui_utils.ems_to_pixels(0.6),
            pady=ui_utils.ems_to_pixels(0.5),
            insertwidth=0,
            highlightthickness=0,
            background=ui_utils.lookup_style_option("ViewToolbar.TFrame", "background"),
        )
        
        for color_name, color in COLORS.items():
            self.header_bar.tag_configure(color_name, foreground=color)
        
        self.header_bar.grid(row=0, column=0, sticky="nsew")
        self.header_bar.set_read_only(True)
        self.menu_button = ttk.Button(
                                header_frame, 
                                text=" ≡ ", 
                                style="ViewToolbar.Toolbutton", 
                                width=3,
                                command=self.post_button_menu
                            )
        self.header_bar.bind("<Configure>", self.resize_header_bar, True)
        self.header_bar.configure(height=1)

        self.menu_button.place(anchor="ne", rely=0, relx=1)
        self.disable_menu()
     
    def post_button_menu(self):
        """
            The handler of the menu button located in the header of the treeview.
            When clicking the menu button a popoup is opened and shows several options.
        """
        self.add_menu_options()
        self.menu.tk_popup(
            self.menu_button.winfo_rootx(),
            self.menu_button.winfo_rooty() + self.menu_button.winfo_height(),
        )
    
    def add_menu_options(self):
        """
            Adds the options inside the menu button.
        """
        self.menu.delete(0, "end") 
         
        self.menu.add_command(label=PLACE_RED_TEST_ON_TOP_LABEL, command=self.sort_by_red_tests)
        self.menu.add_command(label=RESUME_ORIGINAL_ORDER, command=self.remove_sort_filter)
        self.menu.add_separator() 
        self.menu.add_command(label=SHOW_ONLY_RED_TESTS, command=self.show_only_red_tests)
        self.menu.add_command(label=SHOW_ALL_TESTS, command=self.show_all_tests)
        self.menu.add_separator()
        self.menu.add_command(label=GROUP_BY_VERDICTS, command=self.group_by_verdicts)
        self.menu.add_separator()    
        self.menu.add_command(label=EXPAND_TEST_RESULTS, command=self.expand_rows) 
        self.menu.add_command(label=FOLD_TEST_RESULTS, command=self.fold_rows)
        self.menu.add_separator() 
        self.menu.add_command(label=UPDATE_FONT_LABEL, command=self.update_font, accelerator="Shift+f")
        self.menu.add_command(label=INCREASE_SPACE_BETWEEN_ROWS, command=self.increase_row_height, accelerator="Shift+i")
        self.menu.add_command(label=DECREASE_SPACE_BETWEEN_ROWS, command=self.decrease_row_height, accelerator="Shift+d")
        self.menu.add_command(label=REMOVE_ERROR_DETAILS if not get_option(EXCEPTION_DETAIL) else INCLUDE_ERROR_DETAILS, 
                              command=self.remove_error_details)
        self.menu.add_separator()
        self.menu.add_command(label=CLEAR_LABEL, command=self.clear_tree) 
         
    def resize_header_bar(self, event=None):
        """
        Resize the height of the header.
        Always keep this method otherwise the header will take the whole treeview.
        """
        height = self.tk.call((self.header_bar, "count", "-update", "-displaylines", "1.0", "end"))
        self.header_bar.configure(height=height)

    def update_font(self, event=None):
        """
            This is the handler of the `Update the font` option. The handler inserts the 
            time when the treeview was refreshed. 
            
            It also update the font size of the treeview if and 
            only if the font is changed in thonny.
            
            Note : if a row of the treeview is selected so the effect of the selection will 
            be removed after refresh.
        """
        all_childs = get_all_tree_childrens(self.treeview)
        rowheight = ROW_HEIGHT
        if all_childs:
            # on calcule le meilleure height à appliquer pour la treeview.
            # Cela est fait quand la taille de la police a changé dans thonny.
            rowheight = self.get_optimal_row_height(all_childs)
                     
        self.resize_header_bar()
        # on applique la nouvelle police pour la treeview
        self.__observe_font_changing(rowheight=rowheight)
    
    def sort_by_red_tests(self):
        
        # On filtre que les l1doctest qui ont un flag rouge.
        sorted_failed_nodes = [l1doctest for l1doctest in self._copy_l1doctests if l1doctest.get_flag() == L1DocTestFlag.FAILED_FLAG ]
        
        # On met les tests rouges en haut et cela pour tous les l1doctest qui ont au moins un test rouge.
        sorted_failed_tests = []
        for l1doctest in sorted_failed_nodes:
            new_l1doctest = deepcopy(l1doctest)
            new_l1doctest.sort_examples_by_verdicts((FailedVerdict, ExceptionVerdict))
            sorted_failed_tests.append(new_l1doctest)
           
        # On récupère les autres neouds AST 
        others = [l1doctest for l1doctest in self._copy_l1doctests if l1doctest.get_flag() != L1DocTestFlag.FAILED_FLAG]
         # l'addition de tous les noeuds
        sorted_failed_tests.extend(others)

        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            self._copy_l1doctests = sorted_failed_tests
            self.update_tree_contents(sorted_failed_tests)
    
    def remove_sort_filter(self):
        """
        When invoking this method the treeview will restore 
        the original order of its rows.
        """
        def __is_verdicts_copy_equals_to_original():
            if len(self._copy_l1doctests) != len(self._origin_l1doctests):
                return False
            c_names = [c_l1doctest.get_name() for c_l1doctest in self._copy_l1doctests]
            for o_l1doctest in self._origin_l1doctests:
                c_index = c_names.index(o_l1doctest.get_name())
                c_l1doctest = self._copy_l1doctests[c_index]
                if len(c_l1doctest.get_examples()) != len(o_l1doctest.get_examples()): 
                    return False 
            return True
        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            if __is_verdicts_copy_equals_to_original():
                self._copy_l1doctests = self._origin_l1doctests
            self.update_tree_contents(self._copy_l1doctests)
    
    def show_only_red_tests(self):
        from copy import deepcopy
        red_verdicts = (FailedVerdict, FailedWhenExceptionExpectedVerdict, ExceptionVerdict)
        
        only_reds = []
        for l1doctest in self._copy_l1doctests:
            if l1doctest.get_flag() == L1DocTestFlag.FAILED_FLAG:
                red_examples = l1doctest.filter_examples_by_verdicts(red_verdicts)
                new_l1doctest = deepcopy(l1doctest)
                new_l1doctest.set_examples(red_examples)
                only_reds.append(new_l1doctest)
                            
        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            self._copy_l1doctests = only_reds
            self.update_tree_contents(self._copy_l1doctests)
     
    def show_all_tests(self):
        self._copy_l1doctests = self._origin_l1doctests
        self.update_tree_contents(self._copy_l1doctests)
    
    def __group_by_verdicts(self, l1doctests: List[L1DocTest], status_order: List[L1DocTestFlag]=None) -> Dict[L1DocTestFlag, List[L1DocTest]]: 
        """
        Group l1doctests by status and order the statuses according to the provided 
        status order.
        
        :param status_order: A list of L1DocTestFlag that specifies the order in which 
        to group the verdicts by flag.
        :return: A dictionary of verdicts grouped by status.
        """
        status_groups:Dict[L1DocTestFlag, List[L1DocTest]] = {}
        for l1doctest in l1doctests:
            status = l1doctest.get_flag()
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(l1doctest)

        if status_order is None:
            status_order = L1DocTestFlag.get_priorities()
        
        # mettre en ordre les catégories selon l'ordre défini par le paramètre `status_order`
        ordered_groups = {}
        for status in status_order:
            if status in status_groups:
                ordered_groups[status] = status_groups[status]
        status_groups = ordered_groups
        
        return status_groups
    
    def group_by_verdicts(self):  
        grouped = self.__group_by_verdicts(self._origin_l1doctests)
        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            self.clear_tree(clear_all=False) 
            for status, l1doctests in grouped.items():
                row_id = self.insert_row(text=status.short_name(), open=status.should_expand(), 
                                         tags=(status.get_color()))
                self.__add_verdicts_to_treeview(l1doctests, row_id)
     
    def expand_rows(self): 
        """Spreads only the node rows"""
        self.__apply_row_change(True)
    
    def fold_rows(self):
        """Folds only the node rows"""
        self.__apply_row_change(False)
    
    def __apply_row_change(self, to_expand:bool):
        """Depending on the `to_fold` it folds or spreads the rows that
        correspond to the ast nodes.
         
        - If `to_expand` is True, the ast nodes are expanded.
        - If `to_expand` is False, the ast nodes are folded.

        Args:
            to_expand (bool): set to True to expand the rows that correspond
            to the ast nodes. Set to False to fold them.
        """
        if self.treeview.get_children(): # on met à jour que si la treeview possède des éléments
            from copy import copy
            # on sauvegarde la valeur initiale de l'option GLOBAL_VIEW
            initial_val = copy(get_option(GLOBAL_VIEW))
            # on applique la nouvelle valeur de l'option `GLOBAL_VIEW`
            set_option(GLOBAL_VIEW, to_expand)
            # update_tree invoque dynamiquement la valeur de l'option(`GLOBAL_VIEW`) courante
            self.update_tree_contents(self._copy_l1doctests)
            # on restaure la valeur initiale de l'option ??!
            # set_option(GLOBAL_VIEW, initial_val)
    
    def remove_error_details(self):
        if self.treeview.get_children():
            keep_excp_details:bool = get_option(EXCEPTION_DETAIL)
            if keep_excp_details:
                error_view:L1TestErrorView = self.workbench.get_view(L1TestErrorView.__name__)
                error_view.clear()
                error_view.hide_view()
            set_option(EXCEPTION_DETAIL, not keep_excp_details)
            self.update_tree_contents(self._copy_l1doctests)
    
    def increase_row_height(self, event):
        if self.treeview.get_children():
            current_height = self.get_rowheight()
            self.style.configure("Treeview", rowheight=current_height+1)
            self.treeview.update()
    
    def decrease_row_height(self, event):
        if not self.is_empty():
            current_height = self.get_rowheight()
            max_lines = self.__get_longest_wrapped_line()
            opt = self.__compute_optimal_height(max_lines, SMALL_MARGIN)
            print("opt=", opt)
            print("current_height=", current_height)
            if current_height > opt:
                self.style.configure("Treeview", rowheight=current_height-1) 
                self.treeview.update()
        
    def get_rowheight(self):
        return self.style.lookup("Treeview", 'rowheight')
    # -------------------------------------------
    # Fin des fonction pour le Header du treeview
    # ------------------------------------------
    
    def __observe_font_changing(self, event=None, rowheight=ROW_HEIGHT):
        """
            Changes the font of the treeview.
        """
        self.__update_tree_font(get_font_family_option(), 
                                get_font_size_option(), 
                                rowheight=rowheight)
        self.header_bar.config(font=(get_font_family_option(), 
                                     get_font_size_option()))
        return "break"
    
    def __update_tree_font(self, font_family, font_size, rowheight=ROW_HEIGHT):
        """
            Applies the new font to the treeview.
        """
        self.style.configure("Treeview", 
                             justify="left", 
                             rowheight=rowheight, 
                             font=(font_family, font_size), 
                             wrap=tk.WORD)  
    
    def __wrap_tree_content(self, tree: ttk.Treeview, event):
        """
            This function wraps the text of treeview to follow its width.
        """
        widget = event.widget if event else tree
        
        if (isinstance(widget, ttk.Treeview)): 
            if (self.workbench.get_view(self.__class__.__name__).winfo_ismapped()):  
                if not self.is_empty():
                    width = widget.winfo_width()
                    
                    # Une heuristique a été fait pour décider du nombre de caractères par 100 pixels.
                    chars_per_100_pixels = width // (get_font_size_option())
                    
                    childs = get_all_tree_childrens(self.treeview)
                    for iid in childs:
                        text = widget.item(iid)["text"]
                        wrapped = wrap(text, chars_per_100_pixels)   
                        tree.item(iid, text=wrapped)
                    self.reduce_row_spaces(childs, NORMAL_MARGIN) 
        
    def reduce_row_spaces(self, childs, margin=NORMAL_MARGIN):
        all_texts = self.__extract_wrapped_texts(childs)
        max_lines = self.__get_longest_wrapped_line(all_texts)
        opt_height = self.__compute_optimal_height(max_lines, margin)
        self.style.configure("Treeview", rowheight=opt_height)
        self.treeview.update()                
    
    def __extract_wrapped_texts(self, childs:list):
        """
            Returns a list containing all the wrapped texts of all nodes of the treeview.
        """
        return [self.treeview.item(iid)["text"] for iid in childs]
    
    def get_optimal_row_height(self, childs:list):
        """
            Returns the new optimal height.
        """
        all_texts = self.__extract_wrapped_texts(childs)
        
        # Quand le contenu est wrappé, on ajuste la hauteur des lignes, 
        # pour s'assurer que tout le contenu d'une ligne est affichée
        max_lines = self.__get_longest_wrapped_line(all_texts)
        return self.__compute_optimal_height(max_lines)        
        
    def __get_longest_wrapped_line(self, all_texts:list[str]=None):
        """
            Returns the size of the longest wrapped text in the treeview.
        """ 
        if not all_texts:
            childs = get_all_tree_childrens(self.treeview)
            all_texts = self.__extract_wrapped_texts(childs)
        sizes:list = [len(text.split("\n")) for text in all_texts]
        return max(sizes) if sizes else 1
    
    def __compute_optimal_height(self, max_lines:int=None, margin=NORMAL_MARGIN):
        """
            Uses the default font metrics to calculate the optimal row height.
            The default font metrics is multiplied by the given `max_lines`.
            
            The algorithm uses heuristics to calculate the optimal height by eliminating 
            unnecessary padding between rows of the tree as much as possible. 
            
            Args:
                max_lines(int): The number of lines of the longest row in the treeview.
            Return:
                (int): The new height.
        """
        row_height = get_font_size_option() * 2     # multiply by 2 to handle the line spacing
        opt_height = max_lines * (row_height * margin) if max_lines else row_height
        return round(opt_height)
    
    def update_tree_contents(self, l1doctests:List[L1DocTest], parent="", full_clear=True):
        """
            This function contructs and inserts the rows into the treeview.
        """
        def __update_tree_header__():            
            # We build the summarize object 
            summarize: Summarize = self.build_summarize_object(self._origin_l1doctests)
            # We insert the summarize infos into the header bar of the treeview
            self.insert_summarize_in_header_bar(summarize, self.header_bar)
            self.resize_header_bar()
        
        self._restore_row_selection_effect()  
        self.clear_tree(clear_all=full_clear)
   
        if not self.__check_if_editor_is_open():
            return

        self.__add_verdicts_to_treeview(l1doctests, parent)
        
        if self.treeview.get_children():
            __update_tree_header__()
    
    def __add_verdicts_to_treeview(self, l1doctests:List[L1DocTest], parent=""):
        o_names = [c_l1doctest.get_name() for c_l1doctest in self._origin_l1doctests]
        for l1doctest in l1doctests:
            o_index = o_names.index(l1doctest.get_name())
            current_node = self._add_node_to_tree(self._origin_l1doctests[o_index], parent)
            if l1doctest.get_flag() == L1DocTestFlag.EMPTY_FLAG:
                self.treeview.insert(current_node, "end", values=l1doctest.get_node_lineno(), 
                                     text="No tests found", tags=("nonClickable", l1doctest.get_flag().get_color()))
            else:    
                self._add_verdicts_to_node(current_node, l1doctest.get_examples())
         
        self.__wrap_tree_content(self.treeview, None)
        self.enable_menu()
    
    def _add_node_to_tree(self, l1doctest: L1DocTest, parent=""):      
        self.__update_tree_font(get_font_family_option(), get_font_size_option())
                
        flag: L1DocTestFlag = l1doctest.get_flag()
        verdict_config = dict(text=self._get_l1doctest_stats(l1doctest), 
                              image=self.get_icon(flag.name), 
                              open=get_option(GLOBAL_VIEW) if flag == L1DocTestFlag.FAILED_FLAG else False)
        return self.treeview.insert(parent, "end", values=l1doctest.get_node_lineno(), tags=(clickable_tag,), **verdict_config)
    
    def _add_verdicts_to_node(self, current_node:str, examples:list[Example]):
        """ 
        This function adds to the treeview all the rows that correspond 
        to the given ast node.
        """
        def __add_as_many_rows_as_text_lines(parent, text:str, lineno:int, tags:str):
            """
            Adds the necessary rows of each text to be inserted in the treeview.
            An exception message can be reported on several line, so we should 
            add as many rows as text lines. 
            """
            splitted = text.split("\n")
            for line in splitted:
                self.treeview.insert(parent, "end", text=line, values=lineno, tags=tags) 
                
        # insert the sub-rows that represents the verdicts of the executed tests 
        # of the current AST node.
        for example in examples:
            verdict = example.get_verdict()
            item_text = " " + str(verdict)
            verdict_tags = (verdict.get_color(), clickable_tag)
            if isinstance(verdict, FailedVerdict):
                current_test = self.treeview.insert(current_node, "end",  text=item_text, 
                                                    open=get_option(OPEN_RED_ROWS), 
                                                    values=verdict.get_lineno(), tags=verdict_tags)   
                if (isinstance(verdict, FailedWhenExceptionExpectedVerdict)):
                    # le detail d'une `failure` ne doit pas être cliquable
                    verdict_tags = (verdict_tags[0], "nonClickable")
                # a failure message can be reported on several line, so we should add as many rows as text lines. 
                __add_as_many_rows_as_text_lines(current_test, verdict.get_details(), verdict.get_lineno(), tags=verdict_tags)
            elif isinstance(verdict, ExceptionVerdict):
                extra_tags = ("lightred", ) if get_option(HIGHLIGHT_EXCEPTIONS) else ()
                current_test = self.treeview.insert(current_node, "end",  text=item_text, 
                                                    values=[verdict.get_lineno(), verdict.__class__.__name__, verdict.get_details()], 
                                                    tags=verdict_tags+extra_tags,
                                                    open=get_option(OPEN_RED_ROWS))
                # le detail d'une `exception` ne doit pas être cliquable
                error_detail_tags = (verdict_tags[0], "nonClickable")
                
                if not get_option(EXCEPTION_DETAIL):
                    __add_as_many_rows_as_text_lines(current_test, verdict.get_details(), verdict.get_lineno(), tags=error_detail_tags)               
            else :
                current_test = self.treeview.insert(current_node, "end", text=item_text, values=verdict.get_lineno(), tags=verdict_tags)
             
    def insert_row(self, parent="", text="", clear:bool=False, values=(), 
                   open=False, tags:str="", add_empty_line:bool=False):
        """
        Insert a simple row into the treeview. 

        Args:
            text (str): the text to insert. Defaults to "".
            clear (bool): if True the content of the treeview will be cleared before 
                        insert the text. Defaults to False.
            tags (str): any tags supported by the ttk.Treeview. Defaults to "".
            add_empty_line (bool): if True the text will be inserted after an 
                                empty line. Defaults to False.
        """
        if clear:
            self.clear_tree()
        if add_empty_line:
            self.treeview.insert("", "end", text="")    
        
        item = self.treeview.insert(parent, "end", text=text, open=open, tags=tags, values=values)
        self.__wrap_tree_content(self.treeview, None)
        return item
        
    def __check_if_editor_is_open(self) -> bool:
        """
            Returns True if an editor is already opened in thonny. 
            Otherwise, returns False 
        """
        return False if not self.workbench.get_editor_notebook().get_current_editor() else True
    
    def _get_l1doctest_stats(self, l1doctest: L1DocTest):
        """
        Get a string that represents how many tests are passed of the given l1doctest. 
        If the l1docstest is empty, returns only the name of the l1doctest.
        """
        # The first space is necessary so that all text will be aligned
        if l1doctest.get_flag() == L1DocTestFlag.EMPTY_FLAG:
            return " %s" % l1doctest.get_name()
        return " %s ~ %s/%s passed" %(l1doctest.get_name(), l1doctest.count_passed_tests(), l1doctest.count_tests())
        
    def insert_summarize_in_header_bar(self, summarize:Summarize, view: tktextext.TweakableText):
        """
        Builds the summarize test to be inserted in the header of the treeview.
        
        Args:
            summarize (Summarize): a named tuple that contains the summarize infos.
        """
        tests_run = "Tests run: %s\n" % summarize.total
        view.direct_insert("end", tests_run)
        
        insert_label = lambda label, color : view.direct_insert("end", label, tags=(color,)) 
        insert_how_many = lambda how_many, is_last=False: view.direct_insert("end", f"{how_many}" if is_last else f"{how_many}, ")
      
        insert_label("Success: ", "green")
        insert_how_many(summarize.success)
        
        insert_label("Failures: ", "darkred")
        insert_how_many(summarize.failures)
        
        insert_label("Errors: ", "darkred")
        insert_how_many(summarize.errors)
        
        insert_label("Empty: ", "orange")
        insert_how_many(summarize.empty, is_last=True)
            
    def build_summarize_object(self, l1doctests:List[L1DocTest]) -> Summarize:
        """
        Builds the summarize informations. 
        The summarize contains :
            - Total number of executed tests.
            - How many succeed tests, failed tests, error tests and empty tests.
        
        Args:
            results (List[L1DocTest]): all the l1doctests that have been evaluated.

        Returns:
            Summarize: a namedtuple that represents the summarize object.
        """       
        success = sum([l1doctest.count_passed_tests() for l1doctest in l1doctests])
        failures = sum([l1doctest.count_failed_tests() for l1doctest in l1doctests])
        errors = sum([l1doctest.count_error_tests() for l1doctest in l1doctests])
        empty = sum([1 for l1doctest in l1doctests if l1doctest.get_flag() == L1DocTestFlag.EMPTY_FLAG])
        total = success + failures + errors
        return Summarize(total, success, failures, errors, empty)
                   
    def clear_tree(self, event=None, clear_all=True):
        """Clears the treeview by deleting all items. 
        
        Note: this method is also called when the button `clear` is clicked.
        
        Args:
            event: when the button `clear` is clicked the event is not None.
            clear_all: If True, the treeview and the header of the tree will be cleaned.
            if False, only the treeview will be cleaned.
        """
        # on supprime le contenu du header
        if clear_all:
            self.clear_header_bar()
        for child_id in self.treeview.get_children():
            self.treeview.delete(child_id)
        self.disable_menu()
        error_view:L1TestErrorView = self.workbench.get_view(L1TestErrorView.__name__)
        error_view.clear()

    def clear_header_bar(self):
        """Clears the header of the treeview."""
        if self.header_bar:
            self.header_bar.direct_delete("1.0", "end")
            self.resize_header_bar()
    
    def _remove_highlight_selection_effect(self, event=None):
        """
        This function remove the selection effect. When a treeview's row is selected
        it removes the highlight effect on the selected row. So the selected row 
        will look like it is not selected.
        """
        self.style.map('Treeview', background=[], foreground=[])
    
    def _highlight_line_on_editor(self, lineno:int, editor: CodeView):
        """Highlights the line in the editor that corresponds to the selected row in the treeview.

        Args:
            lineno (int): the line number to highlight.
            editor (CodeView): the editor where the line will be highlighted.
        """
        index = editor.text.index(str(lineno) + ".0")
        editor.text.see(index)  # make sure that the double-clicked item is visible
        editor.text.select_lines(lineno, lineno)
    
    def _restore_row_selection_effect(self):
        """
        This function show the selection effect. When a treeview's row is selected
        it shows the highlight effect on the selected row. 
        """
        self.style.map('Treeview', 
                       background=[('selected', 'focus', '#ADD8E6'), ('selected', '!focus', '#D3D3D3')], 
                       foreground=[('selected', 'focus', 'black'), ('selected', '!focus', 'black')])

    
    def _on_select(self, event):
        """
        When a row is selected this function will be triggered. This function highlights 
        the line in the editor that corresponds to the seelcted row in the treeview. 
        """
        self._restore_row_selection_effect()
        editor = self.workbench.get_editor_notebook().get_current_editor()
        if editor:
            code_view = editor.get_code_view()
            focus = self.treeview.focus()
            if not focus: 
                return

            item = self.treeview.item(focus)
            values = item["values"]
            if not values:
                return
                
            if get_option(EXCEPTION_DETAIL): 
                if ExceptionVerdict.__name__ in values:
                    self.workbench.event_generate(L1TREE_VIEW_EVENT, error_title=item["text"],
                                                  error_msg=values[-1], both=True)
                    self.treeview.focus_set()
                        
            lineno = values[0]
            self._highlight_line_on_editor(lineno, code_view)
            self.workbench.event_generate(
                "OutlineDoubleClick", item_text=self.treeview.item(self.treeview.focus(), option="text")
            )

    def disable_menu(self):
        """disable the menu button of the treeview"""
        self.menu_button.state([tk.DISABLED])
        
    def enable_menu(self):
        """enable the menu button of the treeview"""
        self.menu_button.state(["!disabled"])
     
    def insert_in_header(self, text, image:str|tk.PhotoImage=None, clear=False, tags=tuple()):
        """ 
            Inserts text in the header of the treeview. 
            Args:
                text: the text to insert
                image: the basename with it's extension of an image to insert. 
                For example: "info.png". The image must be in the folder `docs/res`.
                clear: if True, the header will be cleared before inserting the text
                tags: the tags to apply to the text. For example: ("red",)
        """
        if clear:
            self.header_bar.direct_delete("1.0", tk.END)
        if image:
            if isinstance(image, str):
                image = self.get_icon(image)
            self.header_bar.image_create(tk.END, image=image)
            text = " " + text
        self.header_bar.direct_insert(tk.END, text, tags=tags)
        self.resize_header_bar()
           
    def is_empty(self):
        return len(self.treeview.get_children()) == 0
    
    def is_header_bar_cleared(self): 
        return not self.header_bar.get("1.0", tk.END).strip("\n")    
    
    def hide_view(self):
        self.workbench.hide_view(self.__class__.__name__)
    
    def show_view(self):
        self.workbench.show_view(self.__class__.__name__)
        
    def set_verdicts(self, verdicts: List[L1DocTest]):
        self._origin_l1doctests = verdicts
        self._copy_l1doctests = self._origin_l1doctests.copy()
    
    def get_treeview(self):
        return self.treeview
    
    def get_icon(self, ref_name:str):
        """
            Returns the image reference saved in the treeview.
        """
        return self.image_references[ref_name]