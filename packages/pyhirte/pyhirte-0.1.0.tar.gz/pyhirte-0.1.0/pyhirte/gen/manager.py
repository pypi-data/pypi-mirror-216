# SPDX-License-Identifier: GPL-2.0-or-later
from typing import Callable
from dasbus.typing import *
from dasbus.connection import MessageBus

from pyhirte.gen.consts import *
from pyhirte.gen.hirte import *


class HirteManager(Hirte):
    def __init__(self, bus: MessageBus = None, use_systembus=True) -> None:
        super().__init__(bus, use_systembus)

        self.manager_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.manager_proxy is None:
            self.manager_proxy = self.bus.get_proxy(
                HIRTE_DBUS_INTERFACE, HIRTE_OBJECT_PATH
            )

        return self.manager_proxy

    def list_units(
        self,
    ) -> List[Tuple[str, str, str, str, str, str, ObjPath, UInt32, str, ObjPath]]:
        return self.get_proxy().ListUnits()

    def list_nodes(self) -> List[Tuple[str, ObjPath, str]]:
        return self.get_proxy().ListNodes()

    def get_node(self, name: str) -> ObjPath:
        return self.get_proxy().GetNode(
            name,
        )

    def create_monitor(self) -> ObjPath:
        return self.get_proxy().CreateMonitor()

    def enable_metrics(self) -> None:
        self.get_proxy().EnableMetrics()

    def disable_metrics(self) -> None:
        self.get_proxy().DisableMetrics()

    def on_job_new(
        self,
        callback: Callable[
            [
                UInt32,
                ObjPath,
            ],
            None,
        ],
    ) -> None:
        """
        callback:
        """
        self.get_proxy().JobNew.connect(callback)

    def on_job_removed(
        self,
        callback: Callable[
            [
                UInt32,
                ObjPath,
                str,
                str,
                str,
            ],
            None,
        ],
    ) -> None:
        """
        callback:
        """
        self.get_proxy().JobRemoved.connect(callback)

    def on_node_connection_state_changed(
        self,
        callback: Callable[
            [
                str,
                str,
            ],
            None,
        ],
    ) -> None:
        """
        callback:
        """
        self.get_proxy().NodeConnectionStateChanged.connect(callback)

    def get_nodes(self) -> List[str]:
        self.get_proxy().Nodes
