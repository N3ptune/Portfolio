from src.project1.fsm import (
    run_fsm,
    Colon,
    WhiteSpace,
    Eof,
    Colon_Dash,
    Comma,
    Comment,
    Undefined,
    Left_Paren,
    Right_Paren,
    Rules,
    Schemes,
    Facts,
    Queries,
    Q_Mark,
    ID,
    Period,
    String,
)
from src.project1.token import Token

# Defines tests for all off the tokens, with pass and fail cases.

class TestColon:
    def test_given_non_colon_when_run_then_reject(self):
        # given
        colon = Colon()
        input_string = "abc  \n \t"

        # when
        number_chars_read, _ = run_fsm(colon, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_colon_when_run_then_accept(self):
        # given
        colon = Colon()
        input_string = ": \r\n\r\n \n \t \t  ab c d"

        # when
        number_chars_read, token = run_fsm(colon, input_string)

        # then
        assert 1 == number_chars_read
        assert str(Token.colon(":")) == str(token)


class TestEof:
    def test_given_non_eof_when_run_then_reject(self):
        # given
        eof = Eof()
        input_string = "abc  \n \t"

        # when
        number_chars_read, _ = run_fsm(eof, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_eof_when_run_then_accept(self):
        # given
        eof = Eof()
        input_string = ""

        # when
        number_chars_read, token = run_fsm(eof, input_string)

        # then
        assert 1 == number_chars_read
        assert str(Token.eof("")) == str(token)


class TestWhiteSpace:
    def test_given_non_white_space_when_run_then_reject(self):
        # given
        whitespace = WhiteSpace()
        input_string = "abc  \n \t"

        # when
        number_chars_read, _ = run_fsm(whitespace, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_white_space_when_run_then_accept(self):
        # given
        whitespace = WhiteSpace()
        input_string = " \r\n\r\n \n \t \t  ab c d"

        # when
        number_chars_read, token = run_fsm(whitespace, input_string)

        # then
        assert 13 == number_chars_read
        assert str(Token.whitespace(" \r\n\r\n \n \t \t  ")) == str(token)


class TestColon_Dash:
    def test_given_non_colon_dash_when_run_then_reject(self):
        # given
        colon_dash = Colon_Dash()
        input_string = ":abc"

        # when
        number_chars_read, _ = run_fsm(colon_dash, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_colon_dash_when_run_then_accept(self):
        # given
        colon_dash = Colon_Dash()
        input_string = ":-:-:-:"

        # when
        number_chars_read, token = run_fsm(colon_dash, input_string)

        # then
        assert 2 == number_chars_read
        assert str(Token.colon_dash(":-")) == str(token)


class TestComma:
    def test_given_non_comma_when_run_then_reject(self):
        # given
        comma = Comma()
        input_string = ".abc,"
        # when
        number_chars_read, _ = run_fsm(comma, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_comma_when_run_then_accept(self):
        # given
        comma = Comma()
        input_string = ",abc,"
        # when
        number_chars_read, token = run_fsm(comma, input_string)

        # then
        assert 1 == number_chars_read
        assert str(Token.comma(",")) == str(token)


class TestComment:
    def test_given_non_comment_when_run_then_reject(self):
        # given
        comment = Comment()
        input_string = "abc \n \t"

        # when
        number_chars_read, _ = run_fsm(comment, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_comment_when_run_then_accept(self):
        # given
        comment = Comment()
        input_string = "#abcdef\n"

        # when
        number_chars_read, token = run_fsm(comment, input_string)

        # then
        assert 7 == number_chars_read
        assert str(Token.comment("#abcdef")) == str(token)


class TestUndefined:
    def test_given_non_undefined_when_run_then_reject(self):
        # given
        undefined = Undefined()
        input_string = "abc \n \t"

        # when
        number_chars_read, _ = run_fsm(undefined, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_undefined_when_run_then_accept(self):
        # given
        undefined = Undefined()
        input_string = "%"

        # when
        number_chars_read, token = run_fsm(undefined, input_string)

        # then
        assert 1 == number_chars_read
        assert str(Token.undefined("%")) == str(token)


class TestFacts:
    def test_given_non_facts_when_run_then_reject(self):
        # given
        facts = Facts()
        input_string = "Schemes"

        # when
        number_chars_read, _ = run_fsm(facts, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_facts_when_run_then_accept(self):
        # given
        facts = Facts()
        input_string = "Facts"

        # when
        number_chars_read, token = run_fsm(facts, input_string)

        # then
        assert 5 == number_chars_read
        assert str(Token.facts("Facts")) == str(token)


class TestID:
    def test_given_non_id_when_run_then_reject(self):
        # given
        id = ID()
        input_string = "%"

        # when
        number_chars_read, _ = run_fsm(id, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_id_when_run_then_accept(self):
        # given
        id = ID()
        input_string = "ID"

        # when
        number_chars_read, token = run_fsm(id, input_string)

        # then
        assert 2 == number_chars_read
        assert str(Token.id("ID")) == str(token)


class TestLeft_Paren:
    def test_given_non_left_paren_when_run_then_reject(self):
        # given
        left_paren = Left_Paren()
        input_string = ")abc"

        # when
        number_chars_read, _ = run_fsm(left_paren, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_left_paren_when_run_then_accept(self):
        # given
        left_paren = Left_Paren()
        input_string = "(abc)"

        # when
        number_chars_read, token = run_fsm(left_paren, input_string)

        # then
        assert 1 == number_chars_read
        assert str(Token.left_paren("(")) == str(token)


class TestQueries:
    def test_given_non_queries_when_run_then_reject(self):
        # given
        queries = Queries()
        input_string = "id"

        # when
        number_chars_read, _ = run_fsm(queries, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_queries_when_run_then_accept(self):
        # given
        queries = Queries()
        input_string = "Queries"

        # when
        number_chars_read, token = run_fsm(queries, input_string)

        # then
        assert 7 == number_chars_read
        assert str(Token.queries("Queries")) == str(token)


class TestPeriod:
    def test_given_non_period_when_run_then_reject(self):
        # given
        period = Period()
        input_string = ",abc"

        # when
        number_chars_read, _ = run_fsm(period, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_period_when_run_then_accept(self):
        # given
        period = Period()
        input_string = ".abc"

        # when
        number_chars_read, token = run_fsm(period, input_string)

        # then
        assert 1 == number_chars_read
        assert str(Token.period(".")) == str(token)


class TestQ_Mark:
    def test_given_non_q_mark_when_run_then_reject(self):
        # given
        q_mark = Q_Mark()
        input_string = "!abc"

        # when
        number_chars_read, _ = run_fsm(q_mark, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_q_mark_when_run_then_accept(self):
        # given
        q_mark = Q_Mark()
        input_string = "?abc"

        # when
        number_chars_read, token = run_fsm(q_mark, input_string)

        # then
        assert 1 == number_chars_read
        assert str(Token.q_mark("?")) == str(token)


class TestRight_Paren:
    def test_given_non_right_paren_when_run_then_reject(self):
        # given
        right_paren = Right_Paren()
        input_string = "(abc)"

        # when
        number_chars_read, _ = run_fsm(right_paren, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_right_paren_when_run_then_accept(self):
        # given
        right_paren = Right_Paren()
        input_string = ")abc("

        # when
        number_chars_read, token = run_fsm(right_paren, input_string)

        # then
        assert 1 == number_chars_read
        assert str(Token.right_paren(")")) == str(token)


class TestRules:
    def test_given_non_rules_when_run_then_reject(self):
        # given
        rules = Rules()
        input_string = "queries"

        # when
        number_chars_read, _ = run_fsm(rules, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_rules_when_run_then_accept(self):
        # given
        rules = Rules()
        input_string = "Rules"

        # when
        number_chars_read, token = run_fsm(rules, input_string)

        # then
        assert 5 == number_chars_read
        assert str(Token.rules("Rules")) == str(token)


class TestSchemes:
    def test_given_non_schemes_when_run_then_reject(self):
        # given
        schemes = Schemes()
        input_string = "Queries"

        # when
        number_chars_read, _ = run_fsm(schemes, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_schemes_when_run_then_accept(self):
        # given
        schemes = Schemes()
        input_string = "Schemes"

        # when
        number_chars_read, token = run_fsm(schemes, input_string)

        # then
        assert 7 == number_chars_read
        assert str(Token.schemes("Schemes")) == str(token)


class TestString:
    def test_given_non_strings_when_run_then_reject(self):
        # given
        string = String()
        input_string = "abc \n \t"

        # when
        number_chars_read, _ = run_fsm(string, input_string)

        # then
        assert 0 == number_chars_read

    def test_given_strings_when_run_then_accept(self):
        # given
        string = String()
        input_string = "'workplz'"

        # when
        number_chars_read, token = run_fsm(string, input_string)

        # then
        assert 9 == number_chars_read
        assert str(Token.string("'workplz'")) == str(token)
