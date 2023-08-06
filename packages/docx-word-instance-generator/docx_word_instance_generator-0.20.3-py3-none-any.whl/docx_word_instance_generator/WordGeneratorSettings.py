import os
from collections.abc import MutableMapping
from typing import Iterator

_KT = str
_VT = any


class WordGeneratorSettings(MutableMapping):
    """
    A custom dictionary allowing you to store program configurations in an easy data structure
    """

    __slots__ = ("config",)

    @property
    def template_docx(self) -> str:
        """

        :return: the file that contains jinja2 tags and that will be used as a template for generating a new docx
        file
        """
        return str(self.config["template_docx"])

    @property
    def output_file(self) -> str:
        """

        :return: an absolute path specifying the path of the output docx that the program will create
        """
        return os.path.abspath(self.config["output_file"])

    @property
    def vars(self):
        """
        :return: dictionary of all the variables that we can use inside the Jinja2 docx template tags
        """
        return dict(self.config["vars"])

    def __init__(self):
        self.config = {}

    def __setitem__(self, __k: _KT, __v: _VT) -> None:
        self.config.__setitem__(__k, __v)

    def __delitem__(self, __v: _KT) -> None:
        del self.config[__v]

    def __getitem__(self, __k: _KT) -> _VT:
        return self.config[__k]

    def __len__(self) -> int:
        return len(self.config)

    def __iter__(self) -> Iterator[_KT]:
        yield from iter(self.config)
