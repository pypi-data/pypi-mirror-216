# SPDX-License-Identifier: GPL-2.0-or-later

from dasbus.client.proxy import InterfaceProxy, ObjectProxy
from dasbus.connection import MessageBus, SystemMessageBus, SessionMessageBus


class Hirte:
    def __init__(self, bus: MessageBus = None, use_systembus=True) -> None:
        self.use_systembus = use_systembus

        if bus is not None:
            self.bus = bus
        elif self.use_systembus:
            self.bus = SystemMessageBus()
        else:
            self.bus = SessionMessageBus()

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        raise Exception("Not implemented!")
