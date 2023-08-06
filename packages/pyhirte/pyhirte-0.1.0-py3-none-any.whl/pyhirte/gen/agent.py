# SPDX-License-Identifier: GPL-2.0-or-later
from typing import Callable
from dasbus.typing import *
from dasbus.connection import MessageBus

from pyhirte.gen.consts import *
from pyhirte.gen.hirte import *


class HirteAgent(Hirte):
    def __init__(self, bus: MessageBus = None, use_systembus=True) -> None:
        super().__init__(bus, use_systembus)

        self.agent_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.agent_proxy is None:
            self.agent_proxy = self.bus.get_proxy(
                HIRTE_AGENT_DBUS_INTERFACE, HIRTE_OBJECT_PATH
            )

        return self.agent_proxy

    def create_proxy(self, local_service_name: str, node: str, unit: str) -> None:
        self.get_proxy().CreateProxy(
            local_service_name,
            node,
            unit,
        )

    def remove_proxy(self, local_service_name: str, node: str, unit: str) -> None:
        self.get_proxy().RemoveProxy(
            local_service_name,
            node,
            unit,
        )
