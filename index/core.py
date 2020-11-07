"""Module that expose the document Index object.
"""
import datetime
import os
import random


class Document(object):

    def __init__(self) -> None:
        super().__init__()


class Index(Document):

    def __init__(self, document: dict) -> None:
        super().__init__()
        self.__document = document

    def _dump_sessions(self):
        today = datetime.date.today()
        for index in range(1, 31):
            filename = os.path.join(
                os.getcwd(), "trainings", f"{today.strftime('%Y')}", f"{today.strftime('%B')}", f"session_{index}.txt"
            )
            with open(filename, "w") as f:
                print("#######" * 7, file=f)
                print(f"[{today.strftime('%B')}](session {index}) - EXERCISES CHESS TRAINING ", file=f)
                print("#######" * 7, file=f)
                print("\n", file=f, end="")
                for _, exercise in enumerate(self.get_exercise_training_list(total=50)):
                    print("\t", _+1, exercise, file=f)

    def dump_txt(self):
        today = datetime.date.today()
        try:
            os.makedirs(os.path.join(os.getcwd(), "trainings", f"{today.strftime('%Y')}", f"{today.strftime('%B')}"))
            self._dump_sessions()
        except FileExistsError as fe:
            print(fe)

    def get_document_property(self, key: str):
        return self.__document.get(key, None)

    def get_list(self, e: dict, key: str, _list: list = None) -> list:
        if not _list:
            _list = []
        if Index._is_section(e) and key == 'sections':
            if not e.get('root', None):
                _list.append(e.get('title'))
        if Index._is_object(e) and key == 'content':
            _list.append(e.get('name'))
        if Index._is_note(e) and key == 'notes':
            _list.append(e.get('text'))
        if e.get(key):
            for _ in e.get(key):
                _list = self.get_list(_, key, _list)
        return _list

    def get_exercise_training(self, _filter=None):
        result = []
        for k, v in self.sections.items():
            result.extend(v)
        training = random.choice(result)
        if _filter is not None:
            if _filter not in training:
                training = self.get_exercise_training(_filter)
        return f"{'White' if random.randint(0, 1) else 'Black'}: {training}"

    def get_exercise_training_list(self, total: int, _filter=None, _sort=False):
        _list = []
        for _ in range(total):
            _list.append(self.get_exercise_training(_filter=_filter))
        if _sort:
            _list.sort()
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
    def index(self):
        return self.get_document_property('index')

    @property
    def training(self):
        return self.get_document_property('trainings')

    @property
    def exercise_list(self):
        return self.get_exercise_training_list(total=10, _filter=None)

    @property
    def plan(self):
        return self.get_document_property('plan')

    @property
    def sections(self):
        section_map = {}
        sections = []
        for e in self.plan.get('sections'):
            sections = self.get_list(e, "sections", sections)
            section_map.__setitem__(e.get('title'), sections)
        return section_map

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
