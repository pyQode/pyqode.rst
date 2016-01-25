import docutils
import mimetypes as mimes
import sys
from pyqode.core import api, modes, panels
from pyqode.rst.backend import server, workers
from pyqode.rst import modes as rstmodes


class RstCodeEdit(api.CodeEdit):
    # generic
    mimetypes = ['text/x-rst']

    for m in mimetypes:
        mimes.add_type(m, '.rst')

    DEFAULT_SERVER = server.__file__

    def __init__(self, parent=None, server_script=None,
                 interpreter=sys.executable, args=None,
                 create_default_actions=True, color_scheme='qt',
                 reuse_backend=False):
        super(RstCodeEdit, self).__init__(parent, create_default_actions)
        if server_script is None:
            server_script = self.DEFAULT_SERVER

        self.backend.start(server_script, interpreter, args,
                           reuse=reuse_backend)
        # append panels
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.SearchAndReplacePanel(),
                           api.Panel.Position.BOTTOM)

        # append modes
        self.modes.append(modes.CursorHistoryMode())
        self.modes.append(modes.CaseConverterMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.CaretLineHighlighterMode())
        self.modes.append(modes.RightMarginMode())
        self.modes.append(rstmodes.RstSH(
            self.document(), color_scheme=api.ColorScheme(color_scheme)))
        self.modes.append(modes.ZoomMode())
        cc = modes.CodeCompletionMode()
        cc.trigger_symbols[:] = []
        self.modes.append(cc)
        self.modes.append(modes.AutoIndentMode())
        self.modes.append(modes.IndenterMode())
        self.modes.append(modes.OccurrencesHighlighterMode())
        self.modes.append(modes.SmartBackSpaceMode())
        self.modes.append(modes.CheckerMode(workers.linter))

        self.panels.append(panels.EncodingPanel(), api.Panel.Position.TOP)
        self.panels.append(panels.ReadOnlyPanel(), api.Panel.Position.TOP)
        self.panels.append(panels.CheckerPanel())

    def setPlainText(self, txt, mime_type='', encoding=''):
        mime_type = self.mimetypes[0]
        try:
            self.syntax_highlighter.set_lexer_from_filename(self.file.path)
        except AttributeError:
            # syntax highlighter removed, e.g. file size > FileManager.limit
            pass
        super(RstCodeEdit, self).setPlainText(txt, mime_type, encoding)

    def to_html(self):
        """
        Return the content of the editor as an html text.
        """
        try:
            return docutils.core.publish_parts(
                self.toPlainText(), source_path=self.file.path,
                writer_name='html', settings_overrides={
                    'output_encoding': 'unicode'})['html_body']
        except docutils.utils.SystemMessage as e:
            return str(e)
