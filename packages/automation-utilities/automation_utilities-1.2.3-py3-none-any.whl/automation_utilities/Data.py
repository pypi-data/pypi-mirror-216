import threading
import json


class Data:
    """This class was made to deal with data used in automation projects"""

    lock = threading.Lock()

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.data = json.load(open(file_name, 'r'))

    def get(self, key):
        if isinstance(self.data[key], int):
            Data.lock.acquire()
            self.data[key] += 1
            json.dump(self.data, open(self.file_name, 'w'), indent=2)
            Data.lock.release()
            return self.data[key] - 1
        else:
            return self.data[key]
