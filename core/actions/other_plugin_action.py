import sys
import argparse
from importlib import import_module
from importlib.metadata import entry_points
from core.constants import ACTION_LINK_PROJECT, ACTION_LIST_PROJECTS, ACTION_EXECUTE, FANDANGO_CMD
from core.db.sqlite_db import check_if_project_exists, get_plugin_manager


def delegate_action_to_plugin():
    """ Deals with actions managed by other plugins """

    invoke_cmd = FANDANGO_CMD + ' ' + sys.argv[1]

    init_parser = argparse.ArgumentParser()
    subparsers = init_parser.add_subparsers()

    ###########################################################################
    #                             Execute parser                              #
    ###########################################################################
    execute_parser = subparsers.add_parser(ACTION_EXECUTE, add_help=False)
    execute_parser.add_argument('--action', help='the name of the action to be performed by the plugin manager\n')
    execute_parser.add_argument('--name', help='the name of the project\n')

    parsed_args, unknown_args = init_parser.parse_known_args(sys.argv[1:])
    parser_used = execute_parser
    exit_with_errors = False

    if '--help' in unknown_args and (not parsed_args.action or not parsed_args.name):
        if not parsed_args.name:
            final_parser = argparse.ArgumentParser(parents=[parser_used],
                                                   usage=f'{invoke_cmd} [--help] --action ACTION_NAME --name PROJECT_NAME',
                                                   epilog=f'Example: {invoke_cmd} --action copy-data --name test_project\n\n',
                                                   add_help=True)
            final_parser.print_help()
            final_parser.exit(0)

        elif parsed_args.name and not parsed_args.action:
            if check_if_project_exists(parsed_args.name):
                # get project plugin manager
                plugin_manager = get_plugin_manager(parsed_args.name)

                if plugin_manager:
                    # import plugin_manager python module
                    plugin_entry_point = entry_points().select(group='fandango.plugin', name=plugin_manager)
                    plugin_module_name = next(iter(plugin_entry_point), None).value
                    plugin_module = import_module(plugin_module_name)
                    plugin_module.Plugin.define_methods()
                    available_actions = '{' + ', '.join(plugin_module.Plugin.get_methods().keys()) + '}'

                    final_parser = argparse.ArgumentParser(parents=[parser_used],
                                                           usage=f'{invoke_cmd} [--help] --action {available_actions} --name PROJECT_NAME',
                                                           add_help=True)
                    final_parser.print_help()
                    final_parser.exit(0)

                else:
                    print(f'The project {parsed_args.name} does not have a plugin manager associated. Execute "{FANDANGO_CMD} {ACTION_LINK_PROJECT} --help" for more details')
                    exit_with_errors = True
            else:
                print(f'There is no project with name {parsed_args.name}. Check the existing projects with "{FANDANGO_CMD} {ACTION_LIST_PROJECTS}"')
                exit_with_errors = True

    else:
        if not parsed_args.name or not parsed_args.action:
            print('You should provide a project name and the action to be performed!')
            exit_with_errors = True

        else:
            if check_if_project_exists(parsed_args.name):
                # get project plugin manager
                plugin_manager = get_plugin_manager(parsed_args.name)

                if plugin_manager:
                    # import plugin_manager python module
                    plugin_entry_point = entry_points().select(group='fandango.plugin', name=plugin_manager)
                    plugin_module_name = next(iter(plugin_entry_point), None).value
                    plugin_module = import_module(plugin_module_name)
                    # define the arguments required by the plugin_manager
                    plugin_module.Plugin.define_args()
                    allowed_args = plugin_module.Plugin.get_args().get(parsed_args.action, [])

                    if allowed_args:
                        final_parser = argparse.ArgumentParser(parents=[parser_used],
                                                               usage=f'{invoke_cmd} [--help] --name PROJECT_NAME {allowed_args["help"]["usage"]}',
                                                               epilog=f'Example: {invoke_cmd} --name test_project {allowed_args["help"]["epilog"]}\n\n',
                                                               add_help=True)

                        for arg_name, arg_info in allowed_args['args'].items():
                            final_parser.add_argument(f'--{arg_name}', help=arg_info['help'], required=arg_info['required'], choices=arg_info.get('choices'))

                        parsed_args = final_parser.parse_args(unknown_args, namespace=parsed_args)

                    plugin_module.Plugin.define_methods()
                    action_method = plugin_module.Plugin.get_methods()[parsed_args.action]
                    print('Performing action...')
                    results = action_method(vars(parsed_args))
                    print('Results:\n', results)

                else:
                    print(f'The project {parsed_args.name} does not have a plugin manager associated. Execute "{FANDANGO_CMD} {ACTION_LINK_PROJECT} --help" for more details')
                    exit_with_errors = True
            else:
                print(f'There is no project with name {parsed_args.name}. Check the existing projects with "{FANDANGO_CMD} {ACTION_LIST_PROJECTS}"')
                exit_with_errors = True

    if exit_with_errors:
        parser_used.exit(1)
    else:
        parser_used.exit(0)
