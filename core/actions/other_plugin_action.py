import sys
import argparse
from importlib import import_module
from importlib.metadata import entry_points
from core import Plugin
from core.constants import ACTION_COPY_DATA, FANDANGO_CMD
from core.db.sqlite_db import update_project


def delegate_action_to_plugin():
    """ Deals with actions managed by other plugins """

    invoke_cmd = FANDANGO_CMD + ' ' + sys.argv[1]

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help=f'action "{ACTION_COPY_DATA}"',
                                       dest='action',
                                       title='Action',
                                       description=f'available actions are "{ACTION_COPY_DATA}"')

    ###########################################################################
    #                           Copy project parser                           #
    ###########################################################################

    copy_parser = subparsers.add_parser(ACTION_COPY_DATA, formatter_class=argparse.RawTextHelpFormatter,
                                        usage=f'{invoke_cmd} [-h] [-n] name [-d] raw_data_path [-p] plugin_name',
                                        epilog=f'Example: {invoke_cmd} -n 202404091 -d /data/Talos/projectx -p irods\n\n',
                                        add_help=False)
    copy_parser.add_argument('-h', '--help', action='store_true', help='show help')
    copy_parser.add_argument('-p', '--plugin', help='plugin to call\n')

    action_to_parser = {ACTION_COPY_DATA: copy_parser}
    parsed_args, unknown_args = parser.parse_known_args(sys.argv[1:])
    action = parsed_args.action
    parser_used = action_to_parser[action]
    exit_with_errors = False

    # set the basic arguments defined in core Plugin class for the action chosen
    Plugin.define_args()
    basic_allowed_args = Plugin.get_args()[parsed_args.action]
    for arg_name, arg_info in basic_allowed_args.items():
        parser_used.add_argument(f'-{arg_name}', f'--{arg_info["long_name"]}', help=arg_info['help'],
                                 required=arg_info['required'], choices=arg_info.get('choices'))

    if parsed_args.help:
        parser_used.print_help()
        parser_used.exit(0)

    if parsed_args.plugin:
        # get python module for plugin selected
        plugin_entry_point = entry_points().select(group='fandango.plugin', name=parsed_args.plugin)

        if plugin_entry_point:
            plugin_module_name = next(iter(plugin_entry_point), None).value
            plugin_module = import_module(plugin_module_name)
            # define the extended arguments required by the plugin selected
            plugin_module.Plugin.define_args()
            extended_allowed_args = plugin_module.Plugin.get_args()[parsed_args.action]

            for arg_name, arg_info in extended_allowed_args.items():
                if arg_name not in basic_allowed_args:
                    parser_used.add_argument(f'-{arg_name}', f'--{arg_info["long_name"]}', help=arg_info['help'],
                                             required=arg_info['required'], choices=arg_info.get('choices'))

            parsed_args = parser_used.parse_args(unknown_args, namespace=parsed_args)

            # define the methods implemented by the plugin selected
            plugin_module.Plugin.define_methods()
            # get the method for the selected action
            action_method = plugin_module.Plugin.get_methods()[parsed_args.action]
            results = action_method(vars(parsed_args))

            if results['success']:
                if action in ACTION_COPY_DATA:
                    update_project(parsed_args.name, 'data_management_system', parsed_args.plugin)

        else:
            print(
                f"ERROR: Couldn't find entrypoint for plugin {parsed_args.plugin}. Looks like either is not installed or you misspelled the plugin name.")
            exit_with_errors = True

    else:
        print('No plugin name provided.')
        exit_with_errors = True

    if exit_with_errors:
        parser_used.exit(1)
    else:
        parser_used.exit(0)
