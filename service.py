#!/usr/bin/env python3

import dbus
import dbus.service
import dbus.mainloop.glib
import json
import logging
import sys

from gi.repository import GLib


class Service(dbus.service.Object):
    memory = {}

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName('cz.posvic.in_memory_storage.service', dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/cz/posvic/in_memory_storage/service')

        self._loop = GLib.MainLoop()
        log.info("service running...")
        self._loop.run()
        log.info("service stopped")

    @dbus.service.method('cz.posvic.in_memory_storage.service.Message', in_signature='s', out_signature='s')
    def message(self, data):
        return self._process(data.split('=', 1))

    @dbus.service.method('cz.posvic.in_memory_storage.service.Quit', in_signature='', out_signature='')
    def quit(self):
        log.info("  shutting down")
        self._loop.quit()

    def _process(self, words):
        if len(words) == 1:
            if words[0] == '[all]':
                return json.dumps(self.memory)
            try:
                log.debug(f"get {words[0]}={self.memory[words[0]]}")
                return self.memory[words[0]]
            except KeyError as e:
                # log.exception(e)
                log.debug(e)
                return "[err]"

        log.debug(f"put {words[0]}={words[1]}")
        self.memory[words[0]] = words[1]
        return "[ok]"


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    log = logging.getLogger()
    # log.setLevel(logging.DEBUG)
    log.setLevel(logging.ERROR)
    log.addHandler(handler)

    Service().run()
