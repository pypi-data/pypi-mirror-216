from itertools import chain


class MissingBehaviour:
    def __init__(self, delta):
        self.delta = delta

    def __bool__(self):
        return not self.delta

    def __str__(self):
        lines = sorted(map(self._to_line, self.delta))
        return "\n  ".join(chain(self._header(), lines))

    def _header(self):
        return ("No missing behaviour" if self else "Missing behaviour:",)

    @staticmethod
    def _to_line(name_and_signature):
        name, signature = name_and_signature
        return f"{name}{signature}"
