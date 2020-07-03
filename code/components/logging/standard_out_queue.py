from multiprocessing import Pipe

read_pipe, write_pipe = None, None


class StandardOutQueue(object):

    def __init__(self):

        global read_pipe, write_pipe
        if read_pipe is None and write_pipe is None:
            read_pipe, write_pipe = Pipe(False)

        self.read_pipe = read_pipe
        self.write_pipe = write_pipe

    def write(self, text):
        self.write_pipe.send(text)

    def read(self):
        if self.read_pipe.poll():
            text = self.read_pipe.recv()
            return text

    def flush(self):
        pass

    def empty(self):
        return not self.read_pipe.poll()
