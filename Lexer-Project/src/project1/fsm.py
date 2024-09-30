"""Finite State Machine (FSM) abstraction.

The finite state machine (FSM) is abstracted by the `FiniteStateMachine` class.
The function `run_fsm(fsm, input_string)` runs the indicated `fsm` until it
accepts or rejects to return the resulting characters read and token.
"""

from typing import Callable
from project1.token import Token


State = Callable[[int, str], "StateAndOutput"]
"""
`State` is a function that takes two inputs and returns a new state with the
new output. The `int` input is the number of characters read. The `str`
input is the character to read. The output is the new state and the new
number of characters read.
"""
StateAndOutput = tuple[State, int]
"""
The `State` is the new state resulting from the input while the `int` is the
new output resulting from the input.
"""


def run_fsm(fsm: "FiniteStateMachine", input_string: str) -> tuple[int, Token]:
    """Run an FSM and return the number of characters read with the token.

    Run the passed in FSM until it accepts or rejects. The output is captured
    on each state transition and passed as input with the next character. It returns
    the number or character read and the resulting token.

    Args:

        fsm: the FSM to run
        input_string: the string to use as input

    Returns:

        (output_num_chars_read, token): the number of characters read from the input and the associated token produced by the FSM as a tuple

    Examples:

        >>> from project1.fsm import run_fsm, Colon
        >>> colon = Colon()
        >>> input_string = ": a"
        >>> number_chars_read, token = run_fsm(colon, input_string)
        >>> "number_chars_read = {} token = {}".format(number_chars_read, str(token))
        'number_chars_read = 1 token = (COLON,":",0)'
    """
    current_state: State = fsm.initial_state
    next_state: State

    output_num_chars_read: int = 0

    input_num_chars_read: int = 0
    input_char: str = ""

    number_of_chars = len(input_string)
    for i in range(0, number_of_chars + 1):
        input_num_chars_read = output_num_chars_read
        input_char = input_string[i] if i < number_of_chars else ""

        next_state, output_num_chars_read = current_state(
            input_num_chars_read, input_char
        )
        if next_state in {
            FiniteStateMachine.s_accept,
            FiniteStateMachine.s_reject,
        }:
            break

        current_state = next_state

    value = input_string[:output_num_chars_read]
    return (output_num_chars_read, fsm.token(value))


class FiniteStateMachine:
    """Base class for the finite state machine (FSM) abstraction.

    The base class defines the accept and reject states. The reject state
    will always return zero characters read. Once accept/reject, then always
    accept/reject. The output does not change once in these states. The
    `token` function should be overridden in each subclass.

    Attributes:
        initial_state (State): The initial state for this FSM.
    """

    __slots__ = ["initial_state"]

    def __init__(self, initial_state: State) -> None:
        """Initialize the FSM with its initial state

        Args:
            initial_state: The initial state for this FSM.
        """
        self.initial_state = initial_state

    def token(self, value: str) -> Token:
        """Return the token produced by this FSM

        NOTE: this method must be overridden in any subclass as it defaults to UNDEFINED

        Args:
            value: The value associated with this `Token`.

        Returns:
            Token.undefined: The method must be overridden in subclasses.
        """
        return Token.undefined(value)

    @staticmethod
    def s_accept(input_chars_read: int, input_char: str) -> StateAndOutput:
        """Accept sync state -- once accept always accept."""
        return FiniteStateMachine.s_accept, input_chars_read

    @staticmethod
    def s_reject(input_chars_read: int, input_char: str) -> StateAndOutput:
        """Reject sync state -- once reject always reject."""
        return FiniteStateMachine.s_reject, input_chars_read


class Colon(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Colon.s_0)

    def token(self, value: str) -> Token:
        """Create a token of type COLON.

        NOTE: the match statement is for mypy as it ensures that mypy is able to statically
        prove that `value` is ":" when calling `Token.colon(value)`. Follow the pattern for
        other keyword FSMs.

        Args:
            value: The characters read by the FSM.

        Returns:
            Token.colon: iff what is read is a ":" otherwise Token.undefined -- both use `value` for the token.
        """
        match value:
            case ":":
                return Token.colon(value)
            case _:
                return super().token(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == ":":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Eof(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Eof.s_0)

    def token(self, value: str) -> Token:
        match value:
            case "":
                return Token.eof(value)
            case _:
                return super().token(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class WhiteSpace(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(WhiteSpace.s_0)

    def token(self, value: str) -> Token:
        return Token.whitespace(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char in [" ", "\t", "\r", "\n"]:
            return WhiteSpace.s_0, input_chars_read + 1
        elif input_chars_read > 0:
            return FiniteStateMachine.s_accept, input_chars_read
        else:
            return FiniteStateMachine.s_reject, 0


class Colon_Dash(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Colon_Dash.s_0)

    def token(self, value: str) -> Token:
        return Token.colon_dash(":-")

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == ":":
            return Colon_Dash.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_1(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "-":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Comma(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Comma.s_0)

    def token(self, value: str) -> Token:
        match value:
            case ",":
                return Token.comma(value)
            case _:
                return super().token(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == ",":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Comment(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Comment.s_0)

    def token(self, value: str) -> Token:
        return Token.comment(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "#":
            return Comment.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_1(input_chars_read: int, input_char: str) -> StateAndOutput:
        # if input_char not in ["\n", "EOF"]:
        #     return Comment.s_1, input_chars_read + 1
        if input_char in ["\n", ""]:
            return FiniteStateMachine.s_accept, input_chars_read
        else:
            return Comment.s_1, input_chars_read + 1


class Undefined(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Undefined.s_0)

    def token(self, value: str) -> Token:
        return Token.undefined(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if (
            input_char
            not in [
                "\n",
                "\r" "\t",
                " ",
                "",
                ",",
                ".",
                "S",
                "R",
                "F",
                "Q",
                "?",
                "'",
                ":",
                "#",
                "(",
                ")",
            ]
            and not input_char.isalpha()
        ):
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Facts(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Facts.s_0)

    def token(self, value: str) -> Token:
        return Token.facts("Facts")

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "F":
            return Facts.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_1(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "a":
            return Facts.s_2, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_2(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "c":
            return Facts.s_3, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_3(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "t":
            return Facts.s_4, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_4(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "s":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class ID(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(ID.s_0)

    def token(self, value: str) -> Token:
        return Token.id(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char.isalpha():
            return ID.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_1(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char.isalnum():
            return ID.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_accept, input_chars_read


class Left_Paren(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Left_Paren.s_0)

    def token(self, value: str) -> Token:
        match value:
            case "(":
                return Token.left_paren(value)
            case _:
                return super().token(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "(":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Period(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Period.s_0)

    def token(self, value: str) -> Token:
        match value:
            case ".":
                return Token.period(value)
            case _:
                return super().token(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == ".":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Queries(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Queries.s_0)

    def token(self, value: str) -> Token:
        return Token.queries("Queries")

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "Q":
            return Queries.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_1(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "u":
            return Queries.s_2, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_2(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "e":
            return Queries.s_3, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_3(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "r":
            return Queries.s_4, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_4(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "i":
            return Queries.s_5, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_5(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "e":
            return Queries.s_6, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_6(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "s":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Q_Mark(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Q_Mark.s_0)

    def token(self, value: str) -> Token:
        match value:
            case "?":
                return Token.q_mark(value)
            case _:
                return super().token(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "?":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Right_Paren(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Right_Paren.s_0)

    def token(self, value: str) -> Token:
        match value:
            case ")":
                return Token.right_paren(value)
            case _:
                return super().token(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == ")":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Rules(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Rules.s_0)

    def token(self, value: str) -> Token:
        return Token.rules("Rules")

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "R":
            return Rules.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_1(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "u":
            return Rules.s_2, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_2(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "l":
            return Rules.s_3, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_3(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "e":
            return Rules.s_4, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_4(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "s":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class Schemes(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(Schemes.s_0)

    def token(self, value: str) -> Token:
        return Token.schemes(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "S":
            return Schemes.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_1(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "c":
            return Schemes.s_2, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_2(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "h":
            return Schemes.s_3, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_3(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "e":
            return Schemes.s_4, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_4(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "m":
            return Schemes.s_5, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_5(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "e":
            return Schemes.s_6, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_6(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "s":
            return FiniteStateMachine.s_accept, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0


class String(FiniteStateMachine):
    def __init__(self) -> None:
        super().__init__(String.s_0)

    def token(self, value: str) -> Token:
        return Token.string(value)

    @staticmethod
    def s_0(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "'":
            return String.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_1(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char not in ["", "\n", "'"]:
            return String.s_1, input_chars_read + 1
        elif input_char == "'":
            return String.s_2, input_chars_read + 1
        else:
            return FiniteStateMachine.s_reject, 0

    @staticmethod
    def s_2(input_chars_read: int, input_char: str) -> StateAndOutput:
        if input_char == "'":
            return String.s_1, input_chars_read + 1
        else:
            return FiniteStateMachine.s_accept, input_chars_read
