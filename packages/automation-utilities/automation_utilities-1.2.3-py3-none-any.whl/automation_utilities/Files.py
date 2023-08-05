import threading


class Files:

    lock = threading.Lock()

    @staticmethod
    def add(text: str, to: str):
        Files.lock.acquire()
        open(to, 'a').write(text)
        Files.lock.release()
