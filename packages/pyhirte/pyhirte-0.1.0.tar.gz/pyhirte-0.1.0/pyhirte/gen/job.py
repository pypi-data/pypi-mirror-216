# SPDX-License-Identifier: GPL-2.0-or-later
from typing import Callable
from dasbus.typing import *
from dasbus.connection import MessageBus

from pyhirte.gen.consts import *
from pyhirte.gen.hirte import *


class HirteJob(Hirte):
    def __init__(
        self, job_path: ObjPath, bus: MessageBus = None, use_systembus=True
    ) -> None:
        super().__init__(bus, use_systembus)

        self.job_path = job_path
        self.job_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.job_proxy is None:
            self.job_proxy = self.bus.get_proxy(HIRTE_DBUS_INTERFACE, self.job_path)

        return self.job_proxy

    def cancel(self) -> None:
        self.get_proxy().Cancel()

    def get_id(self) -> UInt32:
        self.get_proxy().Id

    def get_node(self) -> str:
        self.get_proxy().Node

    def get_unit(self) -> str:
        self.get_proxy().Unit

    def get_job_type(self) -> str:
        self.get_proxy().JobType

    def get_state(self) -> str:
        self.get_proxy().State
