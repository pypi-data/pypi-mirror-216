import unittest
from functools import partial
from unittest.mock import MagicMock

from cloudshell.shell.standards.firewall.driver_interface import (
    FirewallResourceDriverInterface,
)


class TestDriverInterface(unittest.TestCase):
    def test_interface_is_abstract(self):
        with self.assertRaisesRegex(TypeError, "abstract"):
            FirewallResourceDriverInterface()

    def test_interface_have_all_methods(self):
        intr_has_attr = partial(hasattr, FirewallResourceDriverInterface)
        self.assertTrue(intr_has_attr("run_custom_command"))
        self.assertTrue(intr_has_attr("run_custom_config_command"))
        self.assertTrue(intr_has_attr("save"))
        self.assertTrue(intr_has_attr("restore"))
        self.assertTrue(intr_has_attr("get_inventory"))
        self.assertTrue(intr_has_attr("orchestration_restore"))
        self.assertTrue(intr_has_attr("orchestration_save"))
        self.assertTrue(intr_has_attr("health_check"))
        self.assertTrue(intr_has_attr("load_firmware"))
        self.assertTrue(intr_has_attr("shutdown"))

    def test_abstract_methods_return_none(self):
        class TestedClass(FirewallResourceDriverInterface):
            def run_custom_command(self, context, custom_command):
                return super().run_custom_command(context, custom_command)

            def run_custom_config_command(self, context, custom_command):
                return super().run_custom_config_command(context, custom_command)

            def save(
                self, context, folder_path, configuration_type, vrf_management_name
            ):
                return super().save(
                    context, folder_path, configuration_type, vrf_management_name
                )

            def restore(
                self,
                context,
                path,
                configuration_type,
                restore_method,
                vrf_management_name,
            ):
                return super().restore(
                    context,
                    path,
                    configuration_type,
                    restore_method,
                    vrf_management_name,
                )

            def get_inventory(self, context):
                return super().get_inventory(context)

            def orchestration_restore(
                self, context, saved_artifact_info, custom_params
            ):
                return super().orchestration_restore(
                    context, saved_artifact_info, custom_params
                )

            def orchestration_save(self, context, mode, custom_params):
                return super().orchestration_save(context, mode, custom_params)

            def health_check(self, context):
                return super().health_check(context)

            def load_firmware(self, context, path, vrf_management_name):
                return super().load_firmware(context, path, vrf_management_name)

            def shutdown(self, context):
                return super().shutdown(context)

        inst = TestedClass()
        arg = MagicMock()
        self.assertIsNone(inst.run_custom_command(arg, arg))
        self.assertIsNone(inst.run_custom_config_command(arg, arg))
        self.assertIsNone(inst.save(arg, arg, arg, arg))
        self.assertIsNone(inst.restore(arg, arg, arg, arg, arg))
        self.assertIsNone(inst.get_inventory(arg))
        self.assertIsNone(inst.orchestration_restore(arg, arg, arg))
        self.assertIsNone(inst.orchestration_save(arg, arg, arg))
        self.assertIsNone(inst.health_check(arg))
        self.assertIsNone(inst.load_firmware(arg, arg, arg))
        self.assertIsNone(inst.shutdown(arg))
