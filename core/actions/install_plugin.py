import sys
import os
import argparse
import subprocess
import site
from importlib import import_module, reload
from importlib.metadata import entry_points
from core.constants import ACTION_INSTALL_PLUGIN, ACTION_UNINSTALL_PLUGIN, FANDANGO_CMD


def install_plugin_methods():
    """ Deals with plugin installation methods """

    invoke_cmd = FANDANGO_CMD + ' ' + sys.argv[1]

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help=f'action "{ACTION_INSTALL_PLUGIN}" or "{ACTION_UNINSTALL_PLUGIN}"',
                                       dest='action',
                                       title='Action',
                                       description=f'available actions are "{ACTION_INSTALL_PLUGIN}" or "{ACTION_UNINSTALL_PLUGIN}"')

    ############################################################################
    #                              Install parser                              #
    ############################################################################

    install_parser = subparsers.add_parser(ACTION_INSTALL_PLUGIN, formatter_class=argparse.RawTextHelpFormatter,
                                           usage=f'{invoke_cmd} [-h] [-p] plugin_path',
                                           epilog=f'Example: {invoke_cmd} -p /home/user/fandanGO-irods  \n\n',
                                           add_help=False)
    install_parser.add_argument('-h', '--help', action='store_true', help='show help')
    install_parser.add_argument('-p', '--plugin', help='the path of the plugin to install\n')

    ############################################################################
    #                             Uninstall parser                             #
    ############################################################################

    uninstall_parser = subparsers.add_parser(ACTION_UNINSTALL_PLUGIN, formatter_class=argparse.RawTextHelpFormatter,
                                             usage=f'{invoke_cmd} [-h] [-p] plugin_name',
                                             epilog=f'Example: {invoke_cmd} -p fandanGO-irods  \n\n',
                                             add_help=False)
    uninstall_parser.add_argument('-h', '--help', action='store_true', help='show help')
    uninstall_parser.add_argument('-p', '--plugin', help='the name of the plugin to uninstall\n')

    action_to_parser = {ACTION_INSTALL_PLUGIN: install_parser,
                        ACTION_UNINSTALL_PLUGIN: uninstall_parser}
    parsed_args = parser.parse_args(sys.argv[1:])
    action = parsed_args.action
    parser_used = action_to_parser[action]
    exit_with_errors = False

    if parsed_args.help:
        parser_used.print_help()
        parser_used.exit(0)

    if action in ACTION_INSTALL_PLUGIN:
        if parsed_args.plugin:
            print(f'FandanGO will install the plugin placed at {parsed_args.plugin} ...')
            plugin_name = ""

            if os.path.exists(parsed_args.plugin):
                plugin_name = os.path.basename(os.path.abspath(parsed_args.plugin).rstrip('/'))

            if not plugin_name:
                print(f"ERROR: Couldn't find plugin name for source {parsed_args.plugin}")
                exit_with_errors = True

            else:
                cmd = [sys.executable, '-m', 'pip', 'install', '-e', parsed_args.plugin]

                try:
                    subprocess.call(cmd)
                    reload(site)
                    # does this python module looks like a fandanGO plugin?
                    plugin_entry_point = entry_points().select(group='fandango.plugin', name=plugin_name)
                    if plugin_entry_point:
                        plugin_module_name = next(iter(plugin_entry_point), None).value
                        plugin_module = import_module(plugin_module_name)
                        plugin_module.Plugin.get_args()
                        plugin_module.Plugin.get_methods()
                    else:
                        print(f"ERROR: Couldn't find entrypoint for plugin {plugin_name}. Uninstalling it...")
                        cmd = [sys.executable, '-m', 'pip', 'uninstall', plugin_name, '-y']
                        subprocess.call(cmd)
                        exit_with_errors = True

                except AttributeError:
                    print("This does not look like a FandanGO plugin! Uninstalling it...")
                    cmd = [sys.executable, '-m', 'pip', 'uninstall', plugin_name, '-y']
                    subprocess.call(cmd)
                    exit_with_errors = True

        else:
            print('Incorrect usage of command "installpl". Execute "fandanGO installpl --help" or '
                  '"fandanGO --help" for more details')
            exit_with_errors = True

    elif action in ACTION_UNINSTALL_PLUGIN:
        if parsed_args.plugin:
            print(f'FandanGO will uninstall the plugin {parsed_args.plugin} ...')
            cmd = [sys.executable, '-m', 'pip', 'uninstall', parsed_args.plugin]
            subprocess.call(cmd)
        else:
            print('Incorrect usage of command "uninstallpl". Execute "fandanGO uninstallpl --help" or '
                  '"fandanGO --help" for more details')
            exit_with_errors = True

    if exit_with_errors:
        parser_used.exit(1)
    else:
        parser_used.exit(0)
