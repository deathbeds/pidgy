from importnb.utils.pytest_plugin import AlternativeModule, AlternativeSourceText
from .loader import PidginImporter, MarkdownImporter

class PidginModule(AlternativeModule):
    loader = PidginImporter
class MarkdownModule(AlternativeModule):
    loader = MarkdownImporter

class PidginTests(metaclass=AlternativeSourceText):
    modules = PidginModule, MarkdownModule

pytest_collect_file = PidginTests.__call__