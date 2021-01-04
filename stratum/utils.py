import codecs
from hashlib import sha256


class Conversion(object):

    @staticmethod
    def double_sha(value):
        return sha256(sha256(value).digest())

    @staticmethod
    def __convert_types(value, t):
        if t is bytes:
            return str(value).encode("utf-8")
        if t is str:
            if isinstance(value, bytes):
                return value.decode("utf-8")
            return t(value)
        if t is bool:
            options_true = ["yes", "1", 1, True]
            options_false = ["no", "0", 0, False]
            if value in options_true:
                return True
            if value in options_false:
                return False

    def str_bytes(self, value):
        return self.__convert_types(value=value, t=bytes)

    def bytes_str(self, value):
        return self.__convert_types(value=value, t=str)

    def make_bool(self, value):
        return self.__convert_types(value=value, t=bool)

    def to_hex(self, value):
        return codecs.encode(self.__convert_types(value=value, t=str), "hex")

    @staticmethod
    def from_hex(value):
        return bytes.fromhex(value)
