"""
@package parsers

Parsers that handle ontologies input. There are currently two available :
* EL internal syntax
* OWL functional syntax

Some of the input can be dismissed if it does not comply with the EL+ setting.
See the documentation of each parser.

Package toplevel usage :
@code
el_parse(fname)
owl_parse(fname)
@endcode

@see elparser.py
@see owlparser.py

"""

try:
    import elparser
    import owlparser
except ImportError as e:
    import parsers.elparser as elparser
    import parsers.owlparser as owlparser

# characters to remove 
_DISMISS = "-"

def _parse(filename, parser):
    """
    @brief Parses a file.

    @param filename Name of the file to parse
    @param parser Parser to use.

    @return Yields the lines of the file, parsed by the parser.
    Empty lines, comments, or syntax errors are simply dismissed.

    """
    with open(filename, 'r') as f:
        for l in f:
            if len(l) > 2 and "#" not in l:
                # TODO improve syntax
                tmpl = l
                for c in _DISMISS:
                    tmpl = tmpl.replace(c, '')
                tmp = parser.parse(tmpl)
                if tmp is not None:
                    yield tmp

def _unparse(filename, rev_parser, lines):
    """
    @brief Rewrites a file.

    @param lines Iterable of parsed lines.
    """
    with open(filename, 'w') as f:
        for l in lines:
            f.write(rev_parser(l) + "\n")

def el_parse(filename):
    return _parse(filename, elparser.EL_PARSER)

def el_write(filename, lines):
    _unparse(filename, elparser.reverse_parser, lines)

def owl_parse(filename):
    return _parse(filename, owlparser.OWL_PARSER)

def owl_write(filename, lines):
    _unparse(filename, owlparser.reverse_parser, lines)
