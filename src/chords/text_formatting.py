import logging
from enum import Enum

from markdown import Extension, markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor, BacktickInlineProcessor

logger = logging.getLogger(__name__)


class Tag(Enum):
    CODE = r"`"
    DEL = r"\-"
    EM = r"_"
    INS = r"\+"
    MARK = r"="
    STRONG = r"\*"
    # https://www.w3schools.com/TAGS/tag_u.asp
    U = r"\^"
    # https://www.w3schools.com/TAGS/tag_s.asp
    S = r"\~"
    # https://www.w3schools.com/TAGS/tag_q.asp
    Q = r'"'

    @property
    def tag(self):
        return self.name.lower()

    @property
    def char_re(self):
        return self.value

    @property
    def char(self):
        return self.value[-1]


class ProcessorMode(Enum):
    WORD = 170
    SINGLE = 175
    DOUBLE = 180

    @property
    def priority(self) -> int:
        return self.value

    @property
    def code(self):
        return self.name.lower()


class CharToTagInlineProcessor:

    @staticmethod
    def of(tag: Tag, char: str, mode: ProcessorMode) -> SimpleTagInlineProcessor:
        match mode:
            case ProcessorMode.SINGLE:
                return SimpleTagInlineProcessor(r'((?<!{char}){char})([^{char}]+?)\1'.format(char=char), tag.tag)
            case ProcessorMode.DOUBLE:
                return SimpleTagInlineProcessor(r'((?<!{char}){char}{char})([^{char}].+?)\1'.format(char=char), tag.tag)
            case ProcessorMode.WORD:
                return SimpleTagInlineProcessor(r'((?<!{char}){char})([^{char}\s]+?)\1'.format(char=char), tag.tag)
            case _:
                raise ValueError(f"{ProcessorMode.__name__}.{mode} not found")


class TextFormattingMarkdownExtension(Extension):
    __PROCESSOR_MODE = 'mode'
    __ALL_MODES = [mode.code for mode in list(ProcessorMode)]

    __FEATURES_ENABLED = 'features'
    __ALL_FEATURES = [tag.tag for tag in list(Tag)]

    def __init__(self, **kwargs):
        self.config = {
            self.__PROCESSOR_MODE: [
                self.__ALL_MODES,
                f'Select one or more processor modes from {", ".join(self.__ALL_MODES)}. Default is all enabled.'
            ],
            self.__FEATURES_ENABLED: [
                self.__ALL_FEATURES,
                'List of features to enable separated by ",". Unset or ALL for all.'
            ]
        }
        super(TextFormattingMarkdownExtension, self).__init__(**kwargs)

    def _config_as_list(self, key, default) -> list[str]:
        value = self.getConfig(key, default)
        return value if isinstance(value, list) else value.split(",")

    def extendMarkdown(self, md):
        modes = self._config_as_list(self.__PROCESSOR_MODE, self.__ALL_MODES)
        features = self._config_as_list(self.__FEATURES_ENABLED, self.__ALL_FEATURES)

        for config in self.getConfigInfo():
            logger.info(f"Config {config[0]}: {self.getConfig(config[0], "????")} ({config[1]})")

        for feature in features:
            tag = Tag[feature.upper()]
            for mode in modes:
                mode = ProcessorMode[mode.upper()]
                logging.info(f"Registering {tag} for tag {tag.tag} using char {tag.char} and mode {mode}")
                md.inlinePatterns.register(CharToTagInlineProcessor.of(tag, tag.char_re, mode),
                                           f"text-{tag.tag}-{mode.code}", mode.priority)

        # names from md.inlinePatterns._data
        # based on original backtick RE
        BACKTICK3_RE = r'(?:(?<!\\)((?:\\{2})+)(?=`+)|(?<!\\)(`{3})(.+?)(?<!`)\2(?!`))'
        md.inlinePatterns.register(BacktickInlineProcessor(BACKTICK3_RE), 'backtick', 100)

        deregisters = ['em_strong', 'em_strong2']
        for deregister in deregisters:
            md.inlinePatterns.deregister(deregister)
        # features_selected = []
        # for feature in features:
        #     features_selected.append(f"{feature}2")
        #     if not only_doubles:
        #         features_selected.append(f"{feature}1")
        #
        # for simple_name in features_selected:
        #     this_module = sys.modules[__name__]
        #     clazz = simple_name.capitalize() + "InlineProcessor"
        #     if hasattr(this_module, clazz):
        #         logger.info(f"Registering {clazz} text formatter")
        #         clazz = getattr(this_module, clazz)
        #         instance = clazz()
        #         register_name = clazz.__name__.replace("InlineProcessor", "").lower()
        #         md.inlinePatterns.register(instance, register_name, 175)


def makeExtension(**kwargs):
    return TextFormattingMarkdownExtension(**kwargs)


def parse(text: str, **kwargs) -> str:
    return markdown(text, extensions=[TextFormattingMarkdownExtension(**kwargs)])
