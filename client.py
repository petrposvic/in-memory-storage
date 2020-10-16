#!/usr/bin/env python3

import click
import dbus
import logging
import sys


@click.command()
@click.argument('msg')
def send_message(msg):
    bus = dbus.SessionBus()
    service = bus.get_object('cz.posvic.in_memory_storage.service', '/cz/posvic/in_memory_storage/service')
    message = service.get_dbus_method('message', 'cz.posvic.in_memory_storage.service.Message')
    log.info(message(msg))


if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)
    send_message()
