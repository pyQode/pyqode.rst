"""
This module contains a native reStructuredText syntax highlighter.
"""
import re
from PyQt5 import QtGui

from pyqode.core.api import SyntaxHighlighter as BaseSH
from pyqode.core.api import TextBlockHelper


def any(name, alternates):
    """Return a named group pattern matching list of alternates."""
    return "(?P<%s>" % name + "|".join(alternates) + ")"


def make_rst_patterns():
    targets = any("namespace", [r'\.\.\s\[.*\]\s?', r'\.\.\s_.*:.*'])
    directives = any("keyword", [r'\.\.\s.*::'])
    references = any('function', [r'[\w\d#\[\]\*\|]*_\b', r'\|[\w\\s]+\|',
                                  '_?`[^`]+`_?'])
    types = any("type", [r':[^:\(\)]*:'])
    comment = any("comment", [r'^\.\.\s.*$'])
    headers = any('tag', [r'^(=|\+|\*|-|`){3,}$'])
    bold = any('bold', [r'\*\*[^\*]+\*\*'])
    italic = any('italic', [r'\*[^\*]+\*'])
    string = any('string', [r'``[^`]+`*'])

    return re.compile(
        "|".join([targets, directives, string, references, types, bold, italic,
                  comment, headers, any("SYNC", [r"\n"])]))


#
# reStructured text syntax highlighter
#
class RstSH(BaseSH):
    """
    Highlights reStructured text.
    """
    mimetype = 'text/x-rst'

    PROG_HEADER = re.compile(r'^(=|\+|\*|-|`){3,}$')
    PROG_END_STRING = re.compile(r'.*`+')

    PROG = make_rst_patterns()

    # Syntax highlighting states (from one text block to another):
    (NORMAL, INSIDE_HEADER, INSIDE_COMMENT, INSIDE_STRING) = list(range(4))

    def __init__(self, parent, color_scheme=None):
        super(RstSH, self).__init__(parent, color_scheme)
        fmt = self.formats['normal']
        self.bold_fmt = QtGui.QTextCharFormat(fmt)
        self.bold_fmt.setFontWeight(QtGui.QFont.Bold)
        self.formats['bold'] = self.bold_fmt
        self.italic_fmt = QtGui.QTextCharFormat(fmt)
        self.italic_fmt.setFontItalic(True)
        self.formats['italic'] = self.italic_fmt

    def highlight_block(self, text, block):
        prev_block = block.previous()
        prev_state = TextBlockHelper.get_state(prev_block)
        self.setFormat(0, len(text), self.formats["normal"])

        no_formats = True
        match = self.PROG.search(text)
        state = self.NORMAL
        while match:
            for key, value in list(match.groupdict().items()):
                if value:
                    no_formats = False
                    start, end = match.span(key)
                    if key == 'tag' and len(set(text)) != 1:
                        # 2 different characters -> not a header, probably a
                        # table
                        continue
                    self.setFormat(start, end - start,
                                   self.formats[key])
                    if key == 'comment':
                        state = self.INSIDE_COMMENT
                    if key == 'string' and not match.group(0).endswith('`'):
                        state = self.INSIDE_STRING
            match = self.PROG.search(text, match.end())

        if no_formats:
            nblock = block.next()
            indent = len(text) - len(text.lstrip())
            if nblock.isValid() and self.PROG_HEADER.match(nblock.text()) and \
                    len(set(nblock.text())) == 1:
                self.setFormat(0, len(text), self.formats["tag"])
            elif prev_state == self.INSIDE_COMMENT and (
                    indent > 0 or not len(text)):
                self.setFormat(0, len(text), self.formats["comment"])
                state = self.INSIDE_COMMENT
            elif prev_state == self.INSIDE_STRING:
                # check if end string found -> highlight match only otherwise
                # highlight whole line
                match = self.PROG_END_STRING.match(text)
                if match:
                    end = match.end()
                else:
                    state = self.INSIDE_STRING
                    end = len(text)
                self.setFormat(0, end, self.formats["string"])
        TextBlockHelper.set_state(block, state)
