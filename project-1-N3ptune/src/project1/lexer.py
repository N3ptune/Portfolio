"""Turn a input string into a stream of tokens with lexical analysis.

The `lexer(input_string: str)` function is the entry point. It generates a
stream of tokens from the `input_string`.

Examples:

    >>> from project1.lexer import lexer
    >>> input_string = ":\\n  \\n:"
    >>> for i in lexer(input_string):
    ...     print(i)
    ...
    (COLON,":",1)
    (COLON,":",3)
    (EOF,"",3)
"""

from typing import Iterator

from project1.token import Token, TokenType
from project1.fsm import (
    run_fsm,
    FiniteStateMachine,
    Colon,
    Eof,
    WhiteSpace,
    Colon_Dash,
    Comment,
    Comma,
    Undefined,
    Facts,
    ID,
    Left_Paren,
    Period,
    Queries,
    Q_Mark,
    Right_Paren,
    Rules,
    Schemes,
    String,
)


# Determines if this token is the end of the file or an undefined token, in which case the program ends.

def is_last_token(token: Token) -> bool:
    if token.token_type == "EOF" or token.token_type == "UNDEFINED":
        return True
    return False

# Determines which token from FSM reads the most characters, and returns in. In case of a tie, the FSM read first wins.

def get_token(input_string: str, fsms: list[FiniteStateMachine]) -> Token:
    if not input_string:
        return Token.eof("")
    
    max_token: Token = Token.undefined("")
    # max_token: Token = Token.whitespace(input_string)
    max_chars_read = 0
    
    for fsm in fsms:
        # needs to be a Token
        num_char, token = run_fsm(fsm, input_string)
        if num_char > max_chars_read:
            max_chars_read = num_char
            max_token = token

    if max_token.token_type == "UNDEFINED":
        return Token.undefined(input_string[0])

    return max_token

#Determines how many newlines have been read in order to get line count

def get_new_lines(token: str) -> int:
    count = token.count("\n")
    return count

# Produces a stream of tokens from a given input string

def lexer(input_string: str) -> Iterator[Token]:
    fsms: list[FiniteStateMachine] = [
        Colon(),
        Eof(),
        WhiteSpace(),
        Colon_Dash(),
        Comment(),
        Comma(),
        Facts(),
        Left_Paren(),
        Period(),
        Queries(),
        Q_Mark(),
        Right_Paren(),
        Rules(),
        Schemes(),
        String(),
        ID(),
        Undefined(),
    ]
    
    hidden: list[TokenType] = ["WHITESPACE"]
    
    line_num: int = 1
    
    while True:
        token = get_token(input_string, fsms)
        token.line_num = line_num
        line_num = line_num + get_new_lines(token.value)
        input_string = input_string.removeprefix(token.value)
        if token.token_type in hidden:
            continue
        yield token
        if is_last_token(token):
            break
