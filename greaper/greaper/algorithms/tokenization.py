import re
from typing import List, Tuple, Optional

# Token types
WORD = "WORD"
NUMBER = "NUMBER"
SYMBOL = "SYMBOL"
STRING = "STRING"
COMMENT = "COMMENT"
WHITESPACE = "WHITESPACE"
UNKNOWN = "UNKNOWN"

# Regex patterns for advanced tokenization
TOKEN_REGEX = re.compile(
    r"""
    (?P<STRING>
        (?:'[^'\\]*(?:\\.[^'\\]*)*') |           # single-quoted string
        (?:"[^"\\]*(?:\\.[^"\\]*)*") |           # double-quoted string
        (?:'''[\s\S]*?''') |                     # triple-single-quoted string (Python)
        (?:\"\"\"[\s\S]*?\"\"\")                 # triple-double-quoted string (Python)
    )
    | (?P<BLOCK_COMMENT>
        /\*[\s\S]*?\*/                           # C/JavaScript block comment
    )
    | (?P<COMMENT>
        \#.* |                                   # Python comment
        //.*                                     # C++/JavaScript single-line comment
    )
    | (?P<NUMBER>
        \b\d+\.\d+\b |                           # float
        \b\d+\b                                  # integer
    )
    | (?P<WORD>
        \b\w+\b                                  # word/identifier
    )
    | (?P<SYMBOL>
        [^\w\s]                                  # symbol
    )
    | (?P<WHITESPACE>
        \s+                                      # whitespace
    )
    """,
    re.VERBOSE | re.UNICODE,
)

def tokenize_line(line: str, with_types: bool = False) -> List:
    """
    Tokenize a line into advanced tokens.
    If with_types is True, returns list of (token, type) tuples.
    """
    tokens = []
    for match in TOKEN_REGEX.finditer(line):
        for typ in ("STRING", "BLOCK_COMMENT", "COMMENT", "NUMBER", "WORD", "SYMBOL", "WHITESPACE"):
            val = match.group(typ)
            if val is not None:
                if with_types:
                    tokens.append((val, typ))
                else:
                    tokens.append(val)
                break
        else:
            if with_types:
                tokens.append((match.group(0), UNKNOWN))
            else:
                tokens.append(match.group(0))
    return tokens

def tokenize_lines(lines: List[str], with_types: bool = False) -> List[List]:
    """
    Tokenize a list of lines.
    If with_types is True, returns list of lists of (token, type) tuples.
    """
    return [tokenize_line(line, with_types=with_types) for line in lines]

def extract_comments(lines: List[str]) -> List[str]:
    """
    Extract all comment tokens from a list of lines.
    """
    comments = []
    for line in lines:
        for token, typ in tokenize_line(line, with_types=True):
            if typ in ("COMMENT", "BLOCK_COMMENT"):
                comments.append(token)
    return comments

def extract_strings(lines: List[str]) -> List[str]:
    """
    Extract all string tokens from a list of lines.
    """
    strings = []
    for line in lines:
        for token, typ in tokenize_line(line, with_types=True):
            if typ == "STRING":
                strings.append(token)
    return strings

def detect_line_syntax(line: str) -> str:
    """
    Classify a line as 'comment', 'string', 'code', or 'mixed'.
    - 'comment': line is only a comment or block comment
    - 'string': line is only a string
    - 'code': line is only code (words/symbols/numbers)
    - 'mixed': line contains a mix (e.g., code and comment)
    """
    tokens = tokenize_line(line, with_types=True)
    found_types = set(typ for _, typ in tokens if typ != WHITESPACE)
    if not found_types:
        return "code"
    if found_types <= {"COMMENT", "BLOCK_COMMENT"}:
        return "comment"
    if found_types == {"STRING"}:
        return "string"
    if found_types <= {"WORD", "NUMBER", "SYMBOL"}:
        return "code"
    return "mixed"

def is_syntax_match(line: str, syntax_mode: str) -> bool:
    """
    Returns True if the line matches the desired syntax mode.
    syntax_mode: "comment", "string", "code", or "all"
    """
    kind = detect_line_syntax(line)
    if syntax_mode == "all":
        return True
    if syntax_mode == "comment":
        return kind == "comment"
    if syntax_mode == "string":
        return kind == "string"
    if syntax_mode == "code":
        return kind == "code"
    if syntax_mode == "mixed":
        return kind == "mixed"
    return False