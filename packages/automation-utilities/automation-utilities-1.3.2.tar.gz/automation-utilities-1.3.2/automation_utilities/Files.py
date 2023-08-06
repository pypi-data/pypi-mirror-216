import threading

lock = threading.Lock()


def add(text: str, to: str) -> None:
    lock.acquire()
    open(to, 'a').write(text)
    lock.release()


def load(*file_names: str):
    lists = []
    for file_name in file_names:
        lock.acquire()
        lists.append(open(file_name, 'r').read().split('\n'))
        lock.release()
    return lists if len(lists) > 1 else lists[0]


def delete(text: str, from_file: str):
    lock.acquire()
    new_text = open(from_file, 'r').read().replace(text, '')
    open(from_file, 'w').write(new_text)
    lock.release()
