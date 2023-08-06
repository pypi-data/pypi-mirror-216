# SPDX-License-Identifier: GPL-2.0-or-later
from typing import Callable
from dasbus.typing import *
from dasbus.connection import MessageBus

from pyhirte.gen.consts import *
from pyhirte.gen.hirte import *


class HirteNode(Hirte):
    def __init__(
        self, node_name: str, bus: MessageBus = None, use_systembus=True
    ) -> None:
        super().__init__(bus, use_systembus)

        self.node_name = node_name
        self.node_proxy = None

    def get_proxy(self) -> InterfaceProxy | ObjectProxy:
        if self.node_proxy is None:
            manager = self.bus.get_proxy(HIRTE_DBUS_INTERFACE, HIRTE_OBJECT_PATH)

            node_path = manager.GetNode(self.node_name)
            self.node_proxy = self.bus.get_proxy(HIRTE_DBUS_INTERFACE, node_path)

        return self.node_proxy

    def start_unit(self, name: str, mode: str) -> ObjPath:
        return self.get_proxy().StartUnit(
            name,
            mode,
        )

    def stop_unit(self, name: str, mode: str) -> ObjPath:
        return self.get_proxy().StopUnit(
            name,
            mode,
        )

    def reload_unit(self, name: str, mode: str) -> ObjPath:
        return self.get_proxy().ReloadUnit(
            name,
            mode,
        )

    def restart_unit(self, name: str, mode: str) -> ObjPath:
        return self.get_proxy().RestartUnit(
            name,
            mode,
        )

    def get_unit_properties(self, name: str, interface: str) -> Structure:
        return self.get_proxy().GetUnitProperties(
            name,
            interface,
        )

    def get_unit_property(self, name: str, interface: str, property: str) -> Variant:
        return self.get_proxy().GetUnitProperty(
            name,
            interface,
            property,
        )

    def set_unit_properties(
        self, name: str, runtime: bool, keyvalues: List[Tuple[str, Variant]]
    ) -> None:
        self.get_proxy().SetUnitProperties(
            name,
            runtime,
            keyvalues,
        )

    def enable_unit_files(
        self, files: List[str], runtime: bool, force: bool
    ) -> Tuple[bool, List[Tuple[str, str, str]],]:
        return self.get_proxy().EnableUnitFiles(
            files,
            runtime,
            force,
        )

    def disable_unit_files(
        self, files: List[str], runtime: bool
    ) -> List[Tuple[str, str, str]]:
        return self.get_proxy().DisableUnitFiles(
            files,
            runtime,
        )

    def list_units(
        self,
    ) -> List[Tuple[str, str, str, str, str, str, ObjPath, UInt32, str, ObjPath]]:
        return self.get_proxy().ListUnits()

    def reload(self) -> None:
        self.get_proxy().Reload()

    def get_name(self) -> str:
        self.get_proxy().Name

    def get_status(self) -> str:
        self.get_proxy().Status
