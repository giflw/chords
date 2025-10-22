from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor


class BaseInlineProcessor(InlineProcessor):

    def __init__(self, md: Markdown | None = None):
        super().__init__(self._re_string(), md)

    def _re_string(self) -> str:
        raise Exception("Not implemented")
