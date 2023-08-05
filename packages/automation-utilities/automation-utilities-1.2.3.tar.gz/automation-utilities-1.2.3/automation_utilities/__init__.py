import threading
import json


class Data:
    """This class was made to deal with data used in automation projects"""

    lock = threading.Lock()

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.data = json.load(open(file_name, 'r'))
        self._privte = 15

    def get(self, key):
        if isinstance(self.data[key], int):
            Data.lock.acquire()
            self.data[key] += 1
            json.dump(self.data, open(self.file_name, 'w'), indent=2)
            Data.lock.release()
            return self.data[key] - 1
        else:
            return self.data[key]


class Files:
    lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def add(text: str, to: str) -> None:
        Files.lock.acquire()
        open(to, 'a').write(text)
        Files.lock.release()

    @staticmethod
    def load(*file_names: str):
        lists = []
        for file_name in file_names:
            lists.append(open(file_name, 'r').read().split('\n'))
        return lists if len(lists) > 1 else lists[0]


class Input:
    def __init__(self):
        pass

    @staticmethod
    def int_input(prompt: str, default: int) -> int:
        try:
            return int(input(prompt))
        except ValueError:
            return default
