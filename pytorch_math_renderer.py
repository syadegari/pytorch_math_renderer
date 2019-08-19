import re

__all__ = ['torch_doc']

contains = lambda string, substring: string.find(substring) > -1
is_empty_line = lambda string: bool(re.match(r'^$', string) or re.match(r'^\s+$', string))

def modify_subscript(string):
    return string.replace('\_', '_')


def replace_inline_math(string):
    string = '\n'.join(map(lambda line: re.sub(r":math:`(.+?)`", "$\g<1>$", line), string.split('\n')))
    string = modify_subscript(string)
    return string

# def remove_whitespace(string):
#     return '\n'.join(map(lambda line: re.sub(r"^\s+(.+$)", r"\g<1>", line), string.split('\n')))


def replace_math_blocks(string):

    source_lines = string.split('\n')
    target_lines = []

    ix, iy = 0, 0
    while max(ix, iy) < len(source_lines):
        if re.match(r'^.+\.\.\s*math\s*::', source_lines[ix]):
            mathstring = ' $$'
            iy += 1
            while is_empty_line(source_lines[iy]): # skip empty lines that might exists between header and body
                iy += 1
            while not is_empty_line(source_lines[iy]) or iy == len(source_lines):
                mathstring += modify_subscript(source_lines[iy])
                iy += 1
            mathstring += ' $$'
            target_lines.append('>' + mathstring)
            ix = iy
        else:
            target_lines.append(source_lines[ix])
            ix += 1
            iy += 1
    return '\n'.join(target_lines)


# def math_markdown(fn):
#     return replace_inline_math(replace_math_blocks(fn.__doc__))
def indent_if(string, start_with):
    return '\n'.join(map(lambda x: '   ' + x if x[:len(start_with)] == start_with else x, string.split('\n')))

def remove_whitespace_if_contains(string, substr):
    return '\n'.join(map(lambda x: re.sub(r"^\s+(.+)$", "\g<1>", x) if x.find(substr)>-1 else x, string.split('\n')))    

class docs:
    def __init__(self, fn):
        self.text = fn.__doc__
            
    def __repr__(self):
        string = replace_inline_math(replace_math_blocks(self.text))
#         string = string.replace('.. note::', '* ..note')
        string = remove_whitespace_if_contains(string, substr='$')
#         string = indent_if(string, start_with='>>>')
        return string


class markdown_doc(docs):
    def _repr_markdown_(self):
        return super(markdown_doc, self).__repr__()

    
def torch_doc(fn):
    if fn.__doc__ is None:
        return f'no documentation exists for {fn.__name__}'
    return markdown_doc(fn)