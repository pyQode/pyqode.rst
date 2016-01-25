from pyqode.rst.widgets import RstCodeEdit
from pyqode.qt.QtTest import QTest


def test_json_code_edit():
    editor = RstCodeEdit()
    editor.file.open('test/files/demo_ko.rst')
    QTest.qWait(1000)
    assert editor.backend.running
    editor.close()
    assert not editor.backend.running


def test_clone(editor):
    clone = editor.clone()
    assert type(clone) == type(editor)
