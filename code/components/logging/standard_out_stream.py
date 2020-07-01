class StandardOutStream(object):

    def __init__(self, q):
        self.queue = q

    def write(self, t):
        self.queue.append(t)

    def flush(self):
        # TODO implement?
        pass
