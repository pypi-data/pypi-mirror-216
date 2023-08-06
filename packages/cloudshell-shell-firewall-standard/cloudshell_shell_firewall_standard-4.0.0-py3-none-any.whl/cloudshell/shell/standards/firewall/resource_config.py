from __future__ import annotations

from attrs import define

from cloudshell.shell.standards.resource_config_generic_models import (
    GenericBackupConfig,
    GenericCLIConfig,
    GenericConsoleServerConfig,
    GenericSnmpConfig,
)


@define(slots=False, str=False)
class FirewallResourceConfig(
    GenericSnmpConfig, GenericCLIConfig, GenericConsoleServerConfig, GenericBackupConfig
):
    ...
