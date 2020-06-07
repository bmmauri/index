"""Module that expose the document Index object.
"""


class Document(object):

    def __init__(self) -> None:
        super().__init__()


class Index(Document):

    def __init__(self, document: dict) -> None:
        super().__init__()
        self.__document = document

    def get_document_property(self, key: str):
        return self.__document.get(key, None)

    def get_list(self, e: dict, key: str, _list: list = None) -> list:
        if not _list:
            _list = []
        if Index._is_section(e) and key == 'sections':
            _list.append(e.get('title'))
        if Index._is_object(e) and key == 'content':
            _list.append(e.get('name'))
        if Index._is_note(e) and key == 'notes':
            _list.append(e.get('text'))
        if e.get(key):
            for _ in e.get(key):
                _list = self.get_list(_, key, _list)
        return _list

    @classmethod
    def _is_note(cls, e: dict) -> bool:
        return 'notes' in e

    @classmethod
    def _is_object(cls, e: dict) -> bool:
        return 'content' in e

    @classmethod
    def _is_section(cls, e: dict) -> bool:
        return 'sections' in e and 'content' in e

    @property
    def index(self): return self.get_document_property('index')

    @property
    def training(self): return self.get_document_property('trainings')

    @property
    def plan(self): return self.get_document_property('plan')

    @property
    def sections(self):
        sections = []
        for e in self.plan.get('sections'):
            sections = self.get_list(e, "sections", sections)
        return sections

    @property
    def objects(self):
        objects = []
        for e in self.plan.get('sections'):
            if e.get('content'):
                for obj in e.get('content'):
                    if Index._is_object(obj):
                        objects = self.get_list(obj, "content", objects)
        return objects

    @property
    def notes(self):
        notes = []
        for e in self.plan.get('sections'):
            if e.get('content'):
                for item in e.get('content'):
                    if Index._is_object(item):
                        for n in item.get('content'):
                            notes = self.get_list(n, "notes", notes)
        return notes
