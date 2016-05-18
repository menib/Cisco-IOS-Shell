import inject

from cloudshell.networking.networking_resource_driver_interface import NetworkingResourceDriverInterface

from cloudshell.shell.core.context.context_utils import context_from_args
from cloudshell.networking.cisco.ios.cisco_ios_bootstrap import CiscoIOSBootstrap
import cloudshell.networking.cisco.ios.cisco_ios_configuration as config
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface


class CiscoIOSResourceDriver(ResourceDriverInterface, NetworkingResourceDriverInterface):
    def __init__(self):
        bootstrap = CiscoIOSBootstrap()
        bootstrap.add_config(config)
        bootstrap.initialize()

    @context_from_args
    def initialize(self, context):
        """Initialize method
        :type context: cloudshell.shell.core.context.driver_context.InitCommandContext
        """
        return 'Finished initializing'

    def cleanup(self):
        pass

    @context_from_args
    def ApplyConnectivityChanges(self, context, request):
        handler = inject.instance('handler')
        response = handler.apply_connectivity_changes(request)
        handler.logger.info('finished applying connectivity changes responce is:\n{0}'.format(str(response)))
        handler.logger.info('Apply Connectivity changes completed')
        return response

    @context_from_args
    def restore(self, context, path, config_type, restore_method, vrf=None):
        """Restore selected file to the provided destination

        :param path: source config file
        :param config_type: running or startup configs
        :param restore_method: append or override methods
        """

        handler = inject.instance('handler')
        response = handler.restore_configuration(source_file=path, restore_method=restore_method,
                                                 config_type=config_type, vrf=vrf)
        handler.logger.info('Restore completed')
        handler.logger.info(response)

    @context_from_args
    def save(self, context, destination_host, source_filename, vrf=None):
        """Save selected file to the provided destination

        :param source_filename: source file, which will be saved
        :param destination_host: destination path where file will be saved
        """

        handler = inject.instance('handler')
        response = handler.backup_configuration(destination_host, source_filename, vrf)
        handler.logger.info('Save completed')
        return response

    @context_from_args
    def get_inventory(self, context):
        """Return device structure with all standard attributes

        :return: response
        :rtype: string
        """

        handler = inject.instance("handler")
        response = handler.discover_snmp()
        handler.logger.info('Autoload completed')
        return response

    @context_from_args
    def update_firmware(self, context, remote_host, file_path):
        """Upload and updates firmware on the resource

        :param remote_host: path to tftp:// server where firmware file is stored
        :param file_path: firmware file name
        :return: result
        :rtype: string
        """

        handler = inject.instance("handler")
        response = handler.update_firmware(remote_host=remote_host, file_path=file_path)
        handler.logger.info(response)

    @context_from_args
    def send_custom_command(self, context, command):
        """Send custom command

        :return: result
        :rtype: string
        """

        handler = inject.instance("handler")
        response = handler.send_command(command)
        return response

    @context_from_args
    def add_vlan(self, context, ports, vlan_range, port_mode, additional_info):
        """Assign vlan or vlan range to the certain interface

        :return: result
        :rtype: string
        """

        handler = inject.instance("handler")
        result_str = handler.add_vlan(port_list=ports,
                                      vlan_range=vlan_range.replace(' ', ''),
                                      port_mode=port_mode,
                                      qnq=('qnq' in additional_info.lower()))
        handler.logger.info(result_str)

    @context_from_args
    def remove_vlan(self, context, ports, vlan_range, port_mode, additional_info):
        """Remove vlan or vlan range from the certain interface

        :return: result
        :rtype: string
        """

        handler = inject.instance("handler")
        result_str = handler.remove_vlan(port_list=ports,
                                         vlan_range=vlan_range, port_mode=port_mode)
        handler.logger.info(result_str)

    @context_from_args
    def send_custom_config_command(self, context, command):
        """Send custom command in configuration mode

        :return: result
        :rtype: string
        """
        handler = inject.instance("handler")
        result_str = handler.send_config_command(command=command)
        return handler.normalize_output(result_str)

    @context_from_args
    def shutdown(self, context):
        pass
