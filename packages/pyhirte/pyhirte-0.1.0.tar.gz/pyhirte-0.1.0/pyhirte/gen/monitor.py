# SPDX-License-Identifier: GPL-2.0-or-later
from typing import Callable
from dasbus.typing import *
from dasbus.connection import MessageBus

from pyhirte.gen.consts import *
from pyhirte.gen.hirte import *


class HirteMonitor(Hirte):
    def __init__(
        self, monitor_path: ObjPath, bus: MessageBus = None, use_systembus=True
    ) -> None:
        super().__init__(bus, use_systembus)

        self.monitor_path = monitor_path
        self.monitor_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.monitor_proxy is None:
            self.monitor_proxy = self.bus.get_proxy(
                HIRTE_DBUS_INTERFACE, self.monitor_path
            )

        return self.monitor_proxy

    def close(self) -> None:
        self.get_proxy().Close()

    def subscribe(self, node: str, unit: str) -> UInt32:
        return self.get_proxy().Subscribe(
            node,
            unit,
        )

    def unsubscribe(self, id: UInt32) -> None:
        self.get_proxy().Unsubscribe(
            id,
        )

    def subscribe_list(self, targets: Tuple[str, List[str]]) -> UInt32:
        return self.get_proxy().SubscribeList(
            targets,
        )

    def on_unit_properties_changed(
        self,
        callback: Callable[
            [
                str,
                str,
                str,
                Structure,
            ],
            None,
        ],
    ) -> None:
        """
        callback:
        """
        self.get_proxy().UnitPropertiesChanged.connect(callback)

    def on_unit_state_changed(
        self,
        callback: Callable[
            [
                str,
                str,
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
        self.get_proxy().UnitStateChanged.connect(callback)

    def on_unit_new(
        self,
        callback: Callable[
            [
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
        self.get_proxy().UnitNew.connect(callback)

    def on_unit_removed(
        self,
        callback: Callable[
            [
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
        self.get_proxy().UnitRemoved.connect(callback)
