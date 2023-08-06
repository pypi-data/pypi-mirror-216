from __future__ import annotations

from typing import Literal, Optional
import typing

import more_itertools

from .. import types


def skip_whitespace(input_stream: more_itertools.peekable[str]) -> None:
    while (peek := input_stream.peek(None)) and peek.isspace():
        next(input_stream)


def skip_whitespace_and_ensure(input_stream: more_itertools.peekable[str], expected: str) -> None:
    skip_whitespace(input_stream)
    peek = input_stream.peek(None)

    if peek is None:
        raise types.ReaderError('Unexpected EOF')

    if peek != expected:
        raise types.ReaderError(f'Expected {expected}, but got: {peek}')

    next(input_stream)


def ensure_char(
    ensure_char: str,
    input_stream: more_itertools.peekable[str],
    eof_error_p: bool = True,
    recursive_p: bool = False,
) -> None:
    peek = peek_char(True, input_stream, False, 'EOF', recursive_p=recursive_p)

    if peek == 'EOF':
        if eof_error_p:
            raise types.ReaderError('Unexpected EOF')
        return

    if peek != ensure_char:
        raise types.ReaderError(f'Expected {ensure_char}, but got: {peek}')


def peek_char(
    peek_type: None | Literal[True] | str,
    input_stream: more_itertools.peekable[str],
    eof_error_p: bool = True,
    eof_value: Optional[str] = None,
    recursive_p: bool = False,
) -> str:
    """
    PEEK_TYPE:
        None: peek one char and return it
        True: skip whitespace and peek one char and return it
        str: skip until PEEK_TYPE and peek one char and return it

    EOF_ERROR_P:
        True: raise an error when EOF is reached
        False: return EOF_VALUE when EOF is reached
               EOF_VALUE should be specified when EOF_ERROR_P is False
    """
    while True:
        peek = input_stream.peek(None)
        if peek is None:
            break

        if peek_type is None:
            break

        elif peek_type == True:
            if not peek.isspace():
                break

        elif isinstance(peek_type, str):  # pyright: ignore [reportUnnecessaryIsInstance]
            if peek == peek_type:
                break

        else:
            typing.assert_never(peek_type)

        next(input_stream)

    if peek is None:
        if eof_error_p:
            raise types.ReaderError('Unexpected EOF')

        if eof_value is None:
            raise ValueError('eof_value must be specified if eof_error_p is False')

        return eof_value

    return peek
