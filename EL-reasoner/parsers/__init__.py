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
    import el.elparser as elparser
    import el.ellexer as ellexer
    import owl.owlparser as owlparser
    import owl.owllexer as owllexer
except ImportError as e:
    import parsers.el.elparser as elparser
    import parsers.el.ellexer as ellexer
    import parsers.owl.owlparser as owlparser
    import parsers.owl.owllexer as owllexer

# characters to remove
_DISMISS = "-"

def _parse(filename, parser, lexer):
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
                tmp = parser.parse(tmpl, lexer=lexer)
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
    return _parse(filename, elparser.EL_PARSER, ellexer.EL_LEXER)

def el_write(filename, lines):
    _unparse(filename, elparser.reverse_parser, lines)

def owl_parse(filename):
    return _parse(filename, owlparser.OWL_PARSER, owllexer.OWL_LEXER)

def owl_write(filename, lines):
    _unparse(filename, owlparser.reverse_parser, lines)
