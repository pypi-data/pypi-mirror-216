import threading


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
