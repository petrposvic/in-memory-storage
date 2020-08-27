#!/usr/bin/python3


import errno
import json
import logging
import os
import sys


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(handler)

memory = {}


class InMemoryStorageDaemon():
    def __init__(self, fifo):
        self.fifo = fifo

    def __enter__(self):
        try:
            log.debug(f"create fifo '{self.fifo}'")
            os.mkfifo(self.fifo)
        except OSError as oe:
            if oe.errno != errno.EEXIST:
                raise
        return self

    def __exit__(self, type, value, traceback):
        log.debug(f"delete fifo '{self.fifo}'")
        os.remove(self.fifo)

    def loop(self):
        while True:
            output = self._read()
            with open(self.fifo, 'w') as f:
                f.write(output)

    def _read(self):
        with open(self.fifo, 'r') as f:
            while True:
                data = f.read()
                if len(data) == 0:
                    break

                return self._process(data.replace('\n', '').split('=', 1))

    def _process(self, words):
        if len(words) == 1:
            if words[0] == '[all]':
                return json.dumps(memory)
            try:
                log.debug(f"get {words[0]}={memory[words[0]]}")
                return memory[words[0]]
            except KeyError as e:
                log.exception(e)
                return "[err]"

        log.debug(f"put {words[0]}={words[1]}")
        memory[words[0]] = words[1]
        return "[ok]"


if __name__ == '__main__':
    default_filepath = '/tmp/in-memory-storage'
    count = len(sys.argv)
    if count == 1:
        filepath = default_filepath
    elif count == 2:
        filepath = sys.argv[1]
    else:
        print("Usage:")
        print("  {} [filepath]".format(sys.argv[0]))
        print("  (default *filepath* is {})".format(default_filepath))
        print("Example:")
        print("  {} /tmp/custom-named-pipe".format(sys.argv[0]))
        exit(1)

    with InMemoryStorageDaemon(filepath) as daemon:
        daemon.loop()
