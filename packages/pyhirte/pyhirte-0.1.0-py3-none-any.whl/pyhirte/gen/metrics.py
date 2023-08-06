# SPDX-License-Identifier: GPL-2.0-or-later
from typing import Callable
from dasbus.typing import *
from dasbus.connection import MessageBus

from pyhirte.gen.consts import *
from pyhirte.gen.hirte import *


class HirteMetrics(Hirte):
    def __init__(
        self, metrics_path: ObjPath, bus: MessageBus = None, use_systembus=True
    ) -> None:
        super().__init__(bus, use_systembus)

        self.metrics_path = metrics_path
        self.metrics_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.metrics_proxy is None:
            self.metrics_proxy = self.bus.get_proxy(
                HIRTE_DBUS_INTERFACE, self.metrics_path
            )

        return self.metrics_proxy

    def on_start_unit_job_metrics(
        self,
        callback: Callable[
            [
                str,
                str,
                str,
                UInt64,
                UInt64,
            ],
            None,
        ],
    ) -> None:
        """
        callback:
        """
        self.get_proxy().StartUnitJobMetrics.connect(callback)

    def on_agent_job_metrics(
        self,
        callback: Callable[
            [
                str,
                str,
                str,
                UInt64,
            ],
            None,
        ],
    ) -> None:
        """
        callback:
        """
        self.get_proxy().AgentJobMetrics.connect(callback)
