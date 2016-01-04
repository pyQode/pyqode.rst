import restructuredtext_lint

ERRORS_LEVELS = {
    'INFO': 0,
    'WARNING': 1,
    'ERROR': 2,
    'SEVERE': 2
}


def linter(request_data):
    code = request_data['code']
    ret_val = []
    for err in sorted(restructuredtext_lint.lint(code), key=lambda x: x.line):
        ret_val.append((err.message, ERRORS_LEVELS[err.type], err.line - 1))
    return ret_val
