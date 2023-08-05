import json
import threading


class Data:
    """This class was made to deal with data used in automation projects"""

    lock = threading.Lock()

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.data = json.load(open(file_name, 'r'))
        self._privte = 15

    def get(self, key, from_list: list = None):
        if isinstance(self.data[key], int):
            Data.lock.acquire()
            self.data[key] += 1
            json.dump(self.data, open(self.file_name, 'w'), indent=2)
            Data.lock.release()
            try:
                return self.data[key] - 1 if from_list is None else from_list[self.data[key] - 1]
            except IndexError:
                self.reset(key)
                return from_list[self.data[key] - 1]
        else:
            return self.data[key]

    def reset(self, key):
        self.data[key] = 0
        Data.lock.acquire()
        json.dump(self.data, open(self.file_name, 'w'), indent=2)
        Data.lock.release()
