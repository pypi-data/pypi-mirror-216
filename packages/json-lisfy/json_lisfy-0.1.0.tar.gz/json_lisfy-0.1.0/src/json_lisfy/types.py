from typing import Literal
import pydantic


## Exceptions

class LisfyError(Exception):
    pass


class ReaderError(LisfyError):
    pass


## Values

class Value(pydantic.BaseModel):
    def lisfy(self, minify: bool=False) -> str:
        raise NotImplementedError

    def __hash__(self) -> int:
        return str(self.__dict__).__hash__()


class ValueObject(Value):
    value: dict[Value, Value]

    def lisfy(self, minify: bool = False) -> str:
        res = [
            (k.lisfy(minify=minify), v.lisfy(minify=minify))
            for k, v
            in self.value.items()
        ]
        return '(object nil ' + ' '.join(f'(item nil {k} {v})' for k, v in res) + ')'


class ValueArray(Value):
    value: list[Value]

    def lisfy(self, minify: bool=False) -> str:
        res = [x.lisfy(minify=minify) for x in self.value]
        return '(array nil ' + ' '.join(res) + ')'


class ValueString(Value):
    value: str

    def lisfy(self, minify: bool=False) -> str:
        return f'(str nil "{self.value}")'


class ValueInteger(Value):
    value: int

    def lisfy(self, minify: bool=False) -> str:
        return f'(int nil {str(self.value)})'


class ValueFloat(Value):
    value: float

    def lisfy(self, minify: bool=False) -> str:
        return f'(float nil {str(self.value)})'


class ValueSymbol(Value):
    value: Literal['EOF', 'null', 'true', 'false']

    def lisfy(self, minify: bool=False) -> str:
        if self.value == 'EOF':
            raise LisfyError('Cannot lisfy EOF')

        return f'(symbol nil "{self.value}")'
