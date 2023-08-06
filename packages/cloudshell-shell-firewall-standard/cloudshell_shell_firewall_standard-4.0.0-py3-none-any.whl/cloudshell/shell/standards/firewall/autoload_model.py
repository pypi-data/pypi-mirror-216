from cloudshell.shell.standards.autoload_generic_models import (
    GenericChassis,
    GenericModule,
    GenericPort,
    GenericPortChannel,
    GenericPowerPort,
    GenericResourceModel,
    GenericSubModule,
)

__all__ = [
    "FirewallResourceModel",
    "GenericResourceModel",
    "GenericChassis",
    "GenericModule",
    "GenericSubModule",
    "GenericPortChannel",
    "GenericPowerPort",
    "GenericPort",
]


class FirewallResourceModel(GenericResourceModel):
    SUPPORTED_FAMILY_NAMES = ["CS_Firewall"]

    @property
    def entities(self):
        class _FirewallEntities:
            Chassis = GenericChassis
            Module = GenericModule
            SubModule = GenericSubModule
            Port = FirewallPort
            PortChannel = GenericPortChannel
            PowerPort = GenericPowerPort

        return _FirewallEntities


class FirewallPort(GenericPort):
    pass
