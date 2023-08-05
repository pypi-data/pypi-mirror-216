"""
"""

import json
import re
import typing


class Serializer:
    """
    """
    _sbase64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    def __init__(self):
        self._name_exclusions = {}
        self._type_exclusions = {}
        self._encode = True
        self._strict_json = False
        self._safe_deserialize = False

        self._data = []

    @property
    def require_strict_json(self) -> bool:
        """
        Specifies whether to follow strict JSON serialization.
        """
        return self._strict_json
    
    @require_strict_json.setter
    def require_strict_json(self, value: bool) -> None:
        """
        :param value:
        """
        self._strict_json = value

    @property
    def require_safe_deserialize(self) -> bool:
        """
        Specifies whether to check for well-formedness before deserializing.
        """
        return self._safe_deserialize
    
    @require_safe_deserialize.setter
    def require_safe_deserialize(self, value: bool) -> None:
        """
        :param value:
        """
        self._safe_deserialize = value

    @property
    def allow_encoding(self) -> bool:
        """
        Specifies whether results should be encoded.
        """
        return self._encode
    
    @allow_encoding.setter
    def allow_encoding(self, value: bool) -> None:
        """
        :param value:
        """
        self._encode = value
    
    def add_name_exclusion(self, *args: str) -> None:
        """
        Exclude certain named elements from seralization.
        
        :param args:
        """
        for argument in args:
            self._name_exclusions[argument] = True

    def remove_name_exclusion(self, *args: str) -> None:
        """
        Remove exclusion of named elements.
        
        :param args:
        """
        for argument in args:
            self._name_exclusions[argument] = False

    def add_type_exclusion(self, *args: type) -> None:
        """
        Exclude certain data types from serialization.
        
        :param args:
        """
        for argument in args:
            self._type_exclusions[argument] = True

    def remove_type_exclusion(self, *args: type) -> None:
        """
        Remove exclusion of data types.
        
        :param args:
        """
        for argument in args:
            self._type_exclusions[argument] = False

    def seralize(self, obj: object) -> str:
        self._data = []
        self._seralize_node([obj], obj, 0, None)

        sdata = "".join(self._data).replace(",}", "}").replace(",]", "]")[:-1]
        return self.base64encode(sdata) if self.allow_encoding else sdata

    def _seralize_node(self, objects: typing.List[object], start_object: object, depth: int, parent_type: type) -> None:
        """
        :param objects:
        :param start_object:
        :param depth:
        :param parent_type:
        """
        for i in (list(objects) if isinstance(objects, dict) else range(len(objects))):
            if (
                type(objects[i]) not in self._type_exclusions
                and i not in self._name_exclusions
                and not (self._strict_json and isinstance(objects[i], function))
            ):
                if isinstance(objects[i], str):
                    delimiters = ["\"", "\""]
                elif isinstance(objects[i], dict):
                    delimiters = ["{", "}"]
                elif isinstance(objects[i], list):
                    delimiters = ["[", "]"]
                else:
                    delimiters = ["", ""]

                if not (parent_type == dict):
                    self._data.append(delimiters[0])
                else:
                    n = f"\"{i}\"" if isinstance(i, str) else i
                    self._data.append(f"{n}:{delimiters[0]}")

                if isinstance(objects[i], dict):
                    if depth == 0 or objects[i] is not start_object:
                        self._seralize_node(objects[i], None, None, type(objects[i]))
                else:
                    if isinstance(objects[i], str):
                        self._data.append(objects[i].replace("\"", "\\\""))
                    elif isinstance(objects[i], None):
                        self._data.append("null")
                    else:
                        self._data.append(objects[i])

            self._data.append(f"{delimiters[1]},")

    def deserialize(self, obj) -> dict:
        """
        :param obj:
        :return:
        """
        try:
            if self.has_encoding_leader(obj):
                obj = self.base64decode(obj)

            if self._safe_deserialize:
                return self.safe_deserialize(obj)
            else:
                return self.unsafe_deserialize(obj)
        except json.JSONDecodeError:
            return {}
    
    def safe_deserialize(self, obj) -> str:
        """
        :param obj:
        :return:
        """
        try:
            parser = JSONParser()
            parser.parse(obj)
            return eval(obj)
        except json.JSONDecodeError:
            return ""

    def unsafe_deserialize(self, obj):
        """
        :param obj:
        :return:
        """
        try:
            return eval(obj)
        except json.JSONDecodeError:
            return ""

    def has_encoding_leader(self, string: str) -> bool:
        """
        :param string:
        :return:
        """
        return string.find("B64ENC") == 0
    
    def strip_leader(self, string: str) -> str:
        """
        :param string:
        :return:
        """
        return string.replace("B64ENC", "")
    
    def prepend_leader(self, string: str) -> str:
        """
        :param string:
        :return:
        """
        return f"B64ENC{string}"
    
    def base64decode(self, string: str) -> str:
        """
        :param string:
        :return:
        """
        if self.has_encoding_leader(string):
            str_in = self.strip_leader(string)
        else:
            return string
        
        str_in = str_in.replace("=", "")
        str_out = []

        for i in range(0, len(str_in), 4):
            ibits = (
                self._sbase64.index(str_in[i]) << 18
            ) | (
                (self._sbase64.index(str_in[i + 1]) << 12) if (i + 1 < len(str_in)) else 0
            ) | (
                ((self._sbase64.index(str_in[i + 2]) & 0xff) << 6) if (i + 2 < len(str_in)) else 0
            ) | (
                (self._sbase64.index(str_in[i + 3]) & 0xff) if (i + 3 < len(str_in)) else 0
            )

            str_out.append(chr(ibits >> 16 & 0xff))
            str_out.append("" if (i > len(str_in) - 3) else chr(ibits >> 8 & 0xff))
            str_out.append("" if (i > len(str_in) - 4) else chr(ibits & 0xff))

        return "".join(str_out)
    
    def base64encode(self, string: str) -> str:
        """
        :param string:
        :return:
        """
        str_out = []

        for i in range(0, len(string), 3):
            ibits = (
                ord(string[i]) << 16
            ) + (
                ((ord(string[i + 1]) & 0xff) << 8) if (i + 1 < len(string)) else 0
            ) + (
                (ord(string[i + 2]) & 0xff) if (i + 2 < len(string)) else 0
            )

            str_out.append(self._sbase64[ibits >> 18 & 0x3f])
            str_out.append(self._sbase64[ibits >> 12 & 0x3f])
            str_out.append("=" if (i > len(string) - 2) else self._sbase64[ibits >> 6 & 0x3f])
            str_out.append("=" if (i > len(string) - 3) else self._sbase64[ibits & 0x3f])

        return self.prepend_leader("".join(str_out))


class JSONParser:
    """
    """
    def __init__(self):
        self.lexer = None
        self.tokens: typing.List[JSONToken] = []

    def parse(self, string: str) -> str:
        """
        :param string:
        :return:
        """
        self.lexer = JSONLexer(string)

        return self._json()
    
    def look_ahead(self, k: int = 0) -> str:
        """
        :param k:
        :return:
        """
        while len(self.tokens <= k):
            self.tokens.append(self.lexer.next_token())
        return self.tokens[k].typeof
    
    def consume(self, typeof: str) -> None:
        """
        :param typeof:
        :raise json.JSONDecodeError:
        """
        if len(self.tokens) == 0:
            self.tokens.append(self.lexer.next_token())

        if self.tokens[0].typeof == typeof:
            self.tokens.pop(0)
        else:
            raise json.JSONDecodeError(
                f"invalid token encountered while validating string (expected {typeof}, got {self.tokens[0].typeof})"
            )
        
    def _json(self) -> None:
        """
        """
        self._value()
        self.consume("_EOF")

    def _value(self) -> None:
        """
        """
        typeof = self.look_ahead()

        if typeof == "_OBJ_OPEN":
            self._object()
        elif typeof == "_ARR_OPEN":
            self._array()
        elif typeof == "_DIGITS" or typeof == "_NEG":
            self._number()
        elif typeof == "_STRING":
            self.consume("_STRING")
        elif typeof == "_TRUE":
            self.consume("_TRUE")
        elif typeof == "_FALSE":
            self.consume("_FALSE")
        elif typeof == "_NULL":
            self.consume("_NULL")

    def _object(self) -> None:
        """
        """
        self.consume("_OBJ_OPEN")
        
        if self.look_ahead() != "_OBJ_CLOSE":
            self._member()
        while self.look_ahead() != "_OBJ_CLOSE":
            self.consume("_SEP")
            self._member()
        
        self.consume("_OBJ_CLOSE")

    def _member(self) -> None:
        """
        """
        self.consume("_STRING")
        self.consume("_ASSIGN")
        self._value()

    def _array(self) -> None:
        """
        """
        self.consume("_ARR_OPEN")
        
        if self.look_ahead() != "_ARR_CLOSE":
            self._member()
        while self.look_ahead() != "_ARR_CLOSE":
            self.consume("_SEP")
            self._member()
        
        self.consume("_ARR_CLOSE")

    def _number(self) -> None:
        """
        """
        if self.look_ahead() == "_NEG":
            self.consume("_NEG")

        self.consume("_DIGITS")

        if self.look_ahead() == "_DOT":
            self.consume("_DOT")
            self.consume("_DIGITS")

        if self.look_ahead() == "_EXP":
            self.consume("_EXP")
            if self.look_ahead() == "_POS":
                self.consume("_POS")
            elif self.look_ahead() == "_NEG":
                self.consume("_NEG")
            self.consume("_DIGITS")


class JSONLexer:
    """
    """
    def __init__(self, input: str):
        input = re.sub(r"\"([^\"\\]|\\\"|\\)*\"", "S", input)
        input = re.sub(r"[0-9]+", "0", input)

        self.input = input
        self.char_tokens = {
            '{': '_OBJ_OPEN',
            '}': '_OBJ_CLOSE',
            '[': '_ARR_OPEN',
            ']': '_ARR_CLOSE',
            ':': '_ASSIGN',
            ',': '_SEP',
            '.': '_DOT',
            '-': '_NEG',
            '+': '_POS',
            'e': '_EXP',
            'E': '_EXP',
            'S': '_STRING',
            '0': '_DIGITS'
        }
    
    def next_token(self) -> "JSONToken":
        """
        :return:
        :raise json.JSONDecodeError:
        """
        if len(self.input) == 0:
            return JSONToken("_EOF", None)
        
        first = self.input[0]
        if first in self.char_tokens:
            self.input = self.input[1:]
            return JSONToken(self.char_tokens[first], first)
        
        if self.input[:4].lower() == "true":
            self.input = self.input[4:]
            return JSONToken("_TRUE", True)
            
        if self.input[:5].lower() == "false":
            self.input = self.input[:5]
            return JSONToken("_FALSE", True)
        
        if self.input[:4].lower() == "null":
            self.input = self.input[:4]
            return JSONToken("_NULL", True)
        
        raise json.JSONDecodeError(
            f"unexpected character ({first}) encountered while validating string"
        )


class JSONToken:
    """
    """
    def __init__(self, typeof: str, value: typing.Any):
        self.typeof = typeof
        self.value = value
