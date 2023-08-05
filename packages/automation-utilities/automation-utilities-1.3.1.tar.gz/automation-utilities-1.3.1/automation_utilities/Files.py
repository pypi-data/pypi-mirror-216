import threading

lock = threading.Lock()


def add(text: str, to: str) -> None:
    lock.acquire()
    open(to, 'a').write(text)
    lock.release()


def load(*file_names: str):
    lists = []
    for file_name in file_names:
        lists.append(open(file_name, 'r').read().split('\n'))
    return lists if len(lists) > 1 else lists[0]
