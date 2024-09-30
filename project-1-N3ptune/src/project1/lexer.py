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
# import project1.fsm as fsm_stuff


def is_last_token(token: Token) -> bool:
    if token.token_type == "EOF" or token.token_type == "UNDEFINED":
        return True
    return False


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
    # print(max_token.token_type)
    return max_token


def get_new_lines(token: str) -> int:
    count = token.count("\n")
    return count


def lexer(input_string: str) -> Iterator[Token]:
    """Produce a stream of tokens from a given input string.

    Pseudo-code:

    ```
    fsms: list[FiniteStateMachine] = [Colon(), Eof(), WhiteSpace()]
    hidden: list[TokenType] = ["WHITESPACE"]
    line_num: int = 1
    token: Token = Token.undefined("")
    while not _is_last_token(token):
        token = _get_token(input_string, fsms)
        token.line_num = line_num
        line_num = line_num + _get_new_lines(token.value)
        input_string = input_string.removeprefix(token.value)
        if token.token_type in hidden:
            continue
        yield token
    ```

    The `_get_token` function should return the token from the FSM that reads
    the most characters. In the case of two FSMs reading the same number of
    characters, the one that comes first in the list of FSMs, `fsms`, wins.
    Some care must be given to determining when the _last_ token has been
    generated and how to update the new `line_num` for the next token.

    Args:
        input_string: Input string for token generation.

    Yields:
        token: The current token resulting from the string.
    """

    # fsms: list[fsm_stuff.FiniteStateMachine] = [fsm_stuff.Colon(), fsm_stuff.Eof(), fsm_stuff.WhiteSpace(), fsm_stuff.Colon_Dash(), fsm_stuff.Comment(), fsm_stuff.Comma(), fsm_stuff.Facts(), fsm_stuff.ID(), fsm_stuff.Left_Paren(), fsm_stuff.Period(), fsm_stuff.Queries(), fsm_stuff.Q_Mark(), fsm_stuff.Right_Paren(), fsm_stuff.Rules(), fsm_stuff.Schemes(), fsm_stuff.String(), fsm_stuff.Undefined()]
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

    # TODO: remove the `print` statements since they are only here for ruff
    # print(fsms)
    # print(hidden)

    # raise NotImplementedError
