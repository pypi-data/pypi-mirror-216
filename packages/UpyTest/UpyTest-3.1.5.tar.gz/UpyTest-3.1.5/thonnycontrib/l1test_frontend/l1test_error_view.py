from thonny import rst_utils, tktextext, ui_utils
import thonny, tkinter.font as tk_font
from thonny.ui_utils import scrollbar_style
from thonnycontrib.utils import get_font_size_option, get_font_family_option

class L1TestErrorView(tktextext.TextFrame):
    def __init__(self, master=None):
        self.text_frame: tktextext.TextFrame = tktextext.TextFrame.__init__(
            self,
            master,
            text_class=AssistantRstText,
            vertical_scrollbar_style=scrollbar_style("Vertical"),
            horizontal_scrollbar_style=scrollbar_style("Horizontal"),
            horizontal_scrollbar_class=ui_utils.AutoScrollbar,
            read_only=True,
            wrap="word",
            font="TkDefaultFont",
        )
        self.workbench = thonny.get_workbench()
        title_font = tk_font.Font(family=get_font_family_option(),
                                  size=get_font_size_option(),
                                  weight="bold")
        
        self.text.tag_config("green", foreground="darkgreen")
        self.text.tag_config("red", foreground="red")
        self.text.tag_config("darkred", foreground="#d41919")
        self.text.tag_config("yellow", foreground="yellow")  
        
        self.text.tag_configure("title", font=title_font)              
    
    def append_text(self, chars, tags=()):
        self.text.direct_insert("end", chars, tags=tags)
        self._update_font(font_family_opt="io_font_family")

    def write(self, data):
        self.text.set_content(data)

    def append_rst(self, rst, tags=[]):
        tags += ["url"]
        self.text.append_rst(rst, tags)
        
    def _update_font(self, font_family_opt=""):
        self.text.config(font=(get_font_family_option(option=font_family_opt), 
                               get_font_size_option()))

    def clear(self):
        self.write("")
        
    def hide_view(self):
        self.workbench.hide_view(self.__class__.__name__)
    
    def show_view(self):
        self.workbench.show_view(self.__class__.__name__)
        
class AssistantRstText(rst_utils.RstText):
    def configure_tags(self):
        super().configure_tags()
        self.workbench = thonny.get_workbench()
        font = tk_font.Font(
                    family=get_font_family_option(option="io_font_family"),
                    size=get_font_size_option(),
                    underline=True
                )
        
        self.tag_configure("url", font=font)

        self.tag_raise("sel")