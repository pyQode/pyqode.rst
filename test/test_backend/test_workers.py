from pyqode.rst.backend.workers import linter


def test_linter_valid():
    with open('test/files/demo_ok.rst', 'r') as f:
        code = f.read()
    errors = linter({'code': code})
    assert len(errors) == 0


def test_linter_invalid():
    with open('test/files/demo_ko.rst', 'r') as f:
        code = f.read()
    errors = linter({'code': code})
    assert len(errors) > 0
