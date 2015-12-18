"""
This module contains a native reStructuredText syntax highlighter.
"""
import re
from pyqode.core.api import SyntaxHighlighter as BaseSH
from pyqode.core.api import TextBlockHelper


#
# reStructured text syntax highlighter
#
class RstSH(BaseSH):
    """
    Highlights reStructured text.
    """
    mimetype = 'text/x-rst'

    # Syntax highlighting states (from one text block to another):
    (NORMAL, INSIDE_STRING, INSIDE_COMMENT, INSIDE_CODE_BLOCK) = list(range(4))

    def __init__(self, parent, color_scheme=None):
        super(RstSH, self).__init__(parent, color_scheme)

    def highlight_block(self, text, block):
        prev_block = block.previous()
        prev_state = TextBlockHelper.get_state(prev_block)
        if prev_state == self.INSIDE_STRING:
            offset = -3
            text = r'`` ' + text
        elif prev_state == self.INSIDE_COMMENT:
            offset = -3
            text = r".. " + text
        else:
            offset = 0

        self.setFormat(0, len(text), self.formats["normal"])

        state = self.NORMAL
        match = self.PROG.search(text)
        while match:
            for key, value in list(match.groupdict().items()):
                print(key, value)
            # next match
            match = self.PROG.search(text, match.end())
        TextBlockHelper.set_state(block, state)
