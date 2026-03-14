from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterator, List, Tuple

MAX_VARIABLES = 5
ALLOWED_VARIABLES = frozenset({"a", "b", "c", "d", "e"})
TOKEN_LPAREN = "("
TOKEN_RPAREN = ")"
TOKEN_NOT = "!"
TOKEN_AND = "&"
TOKEN_OR = "|"
TOKEN_IMPLIES = "->"
TOKEN_EQUIV = "~"
TOKEN_CONST_0 = "0"
TOKEN_CONST_1 = "1"

CHAR_REPLACEMENTS = {
    " ": "",
    "\t": "",
    "\n": "",
    "\r": "",
    "\u2227": TOKEN_AND,
    "\u2228": TOKEN_OR,
    "\u00ac": TOKEN_NOT,
    "\u2192": TOKEN_IMPLIES,
    "\u21d2": TOKEN_IMPLIES,
    "\u2194": TOKEN_EQUIV,
    "\u2261": TOKEN_EQUIV,
}


class LogicSyntaxError(ValueError):
    """Raised when an expression cannot be parsed."""


@dataclass(frozen=True)
class ExprNode:
    def evaluate(self, variable_values: Dict[str, bool]) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class ConstantNode(ExprNode):
    value: bool

    def evaluate(self, variable_values: Dict[str, bool]) -> bool:
        return self.value


@dataclass(frozen=True)
class VariableNode(ExprNode):
    name: str

    def evaluate(self, variable_values: Dict[str, bool]) -> bool:
        if self.name not in variable_values:
            raise LogicSyntaxError(f"Missing value for variable '{self.name}'")
        return variable_values[self.name]


@dataclass(frozen=True)
class NotNode(ExprNode):
    operand: ExprNode

    def evaluate(self, variable_values: Dict[str, bool]) -> bool:
        return not self.operand.evaluate(variable_values)


@dataclass(frozen=True)
class BinaryOpNode(ExprNode):
    operator: str
    left: ExprNode
    right: ExprNode

    def evaluate(self, variable_values: Dict[str, bool]) -> bool:
        left_value = self.left.evaluate(variable_values)
        right_value = self.right.evaluate(variable_values)

        if self.operator == TOKEN_AND:
            return left_value and right_value
        if self.operator == TOKEN_OR:
            return left_value or right_value
        if self.operator == TOKEN_IMPLIES:
            return (not left_value) or right_value
        if self.operator == TOKEN_EQUIV:
            return left_value == right_value
        raise LogicSyntaxError(f"Unsupported binary operator '{self.operator}'")


@dataclass(frozen=True)
class ParsedExpression:
    source: str
    normalized: str
    tokens: Tuple[str, ...]
    root: ExprNode
    variables: Tuple[str, ...]

    def evaluate(self, variable_values: Dict[str, bool]) -> bool:
        return self.root.evaluate(variable_values)


class _Parser:
    def __init__(self, tokens: List[str]):
        self._tokens = tokens
        self._position = 0

    def parse(self) -> ExprNode:
        expression = self._parse_equivalence()
        if self._has_more():
            current_token = self._peek()
            raise LogicSyntaxError(
                f"Unexpected token '{current_token}' at position {self._position}"
            )
        return expression

    def _parse_equivalence(self) -> ExprNode:
        left = self._parse_implication()
        while self._match(TOKEN_EQUIV):
            right = self._parse_implication()
            left = BinaryOpNode(TOKEN_EQUIV, left, right)
        return left

    def _parse_implication(self) -> ExprNode:
        left = self._parse_or()
        if self._match(TOKEN_IMPLIES):
            right = self._parse_implication()
            return BinaryOpNode(TOKEN_IMPLIES, left, right)
        return left

    def _parse_or(self) -> ExprNode:
        left = self._parse_and()
        while self._match(TOKEN_OR):
            right = self._parse_and()
            left = BinaryOpNode(TOKEN_OR, left, right)
        return left

    def _parse_and(self) -> ExprNode:
        left = self._parse_unary()
        while self._match(TOKEN_AND):
            right = self._parse_unary()
            left = BinaryOpNode(TOKEN_AND, left, right)
        return left

    def _parse_unary(self) -> ExprNode:
        if self._match(TOKEN_NOT):
            return NotNode(self._parse_unary())
        if self._match(TOKEN_LPAREN):
            expression = self._parse_equivalence()
            self._expect(TOKEN_RPAREN)
            return expression

        current_token = self._peek()
        if current_token in {TOKEN_CONST_0, TOKEN_CONST_1}:
            self._advance()
            return ConstantNode(current_token == TOKEN_CONST_1)
        if current_token in ALLOWED_VARIABLES:
            self._advance()
            return VariableNode(current_token)

        raise LogicSyntaxError(
            f"Unexpected token '{current_token}' at position {self._position}"
        )

    def _peek(self) -> str:
        if not self._has_more():
            return "<end>"
        return self._tokens[self._position]

    def _advance(self) -> str:
        token = self._peek()
        self._position += 1
        return token

    def _match(self, token: str) -> bool:
        if self._peek() != token:
            return False
        self._position += 1
        return True

    def _expect(self, token: str) -> None:
        if self._match(token):
            return
        raise LogicSyntaxError(
            f"Expected token '{token}' at position {self._position}, found '{self._peek()}'"
        )

    def _has_more(self) -> bool:
        return self._position < len(self._tokens)


def parse_logical_expression(source: str) -> ParsedExpression:
    if source is None:
        raise LogicSyntaxError("Expression cannot be None")

    normalized = _normalize(source)
    tokens = list(_tokenize(normalized))
    if not tokens:
        raise LogicSyntaxError("Expression is empty")

    variables = sorted({token for token in tokens if token in ALLOWED_VARIABLES})
    if len(variables) > MAX_VARIABLES:
        raise LogicSyntaxError(
            f"Too many variables: {len(variables)}. Maximum is {MAX_VARIABLES}"
        )

    parser = _Parser(tokens)
    root = parser.parse()

    return ParsedExpression(
        source=source,
        normalized=normalized,
        tokens=tuple(tokens),
        root=root,
        variables=tuple(variables),
    )


def _normalize(source: str) -> str:
    normalized = source
    for original, replacement in CHAR_REPLACEMENTS.items():
        normalized = normalized.replace(original, replacement)
    return normalized.lower()


def _tokenize(normalized: str) -> Iterator[str]:
    position = 0
    while position < len(normalized):
        char = normalized[position]

        if char == "-":
            if position + 1 < len(normalized) and normalized[position + 1] == ">":
                position += 2
                yield TOKEN_IMPLIES
                continue
            raise LogicSyntaxError(
                f"Unexpected '-' at position {position}. Use '->' for implication."
            )

        if char in {
            TOKEN_LPAREN,
            TOKEN_RPAREN,
            TOKEN_NOT,
            TOKEN_AND,
            TOKEN_OR,
            TOKEN_EQUIV,
            TOKEN_CONST_0,
            TOKEN_CONST_1,
        }:
            position += 1
            yield char
            continue

        if char in ALLOWED_VARIABLES:
            position += 1
            yield char
            continue

        if char.isalpha():
            raise LogicSyntaxError(
                f"Unsupported variable '{char}' at position {position}. "
                "Allowed variables are a, b, c, d, e."
            )

        raise LogicSyntaxError(f"Unexpected character '{char}' at position {position}")
