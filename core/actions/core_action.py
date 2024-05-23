import sys
import argparse
import datetime
from tabulate import tabulate
from importlib.metadata import entry_points
from core.constants import ACTION_CREATE_PROJECT, ACTION_DELETE_PROJECT, ACTION_LIST_PROJECTS, ACTION_LINK_PROJECT, FANDANGO_CMD
from core.db.sqlite_db import create_new_project, delete_project, list_projects, update_project

def perform_core_action():
    """ Deals with core basic actions """

    invoke_cmd = FANDANGO_CMD + ' ' + sys.argv[1]

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='action')

    ###########################################################################
    #                          Create project parser                          #
    ###########################################################################

    create_parser = subparsers.add_parser(ACTION_CREATE_PROJECT,
                                          usage=f'{invoke_cmd} [--help] --name PROJECT_NAME',
                                          epilog=f'Example: {invoke_cmd} --name test_project  \n\n',
                                          add_help=False)
    create_parser.add_argument('--help', action='store_true', help='show help')
    create_parser.add_argument('--name', help='the name of the project to create\n')

    ###########################################################################
    #                          Delete project parser                          #
    ###########################################################################

    delete_parser = subparsers.add_parser(ACTION_DELETE_PROJECT,
                                          usage=f'{invoke_cmd} [--help] [--name] PROJECT_NAME',
                                          epilog=f'Example: {invoke_cmd} --name test_project  \n\n',
                                          add_help=False)
    delete_parser.add_argument('--help', action='store_true', help='show help')
    delete_parser.add_argument('--name', help='the name of the project to delete\n')

    ###########################################################################
    #                           List projects parser                          #
    ###########################################################################

    list_parser = subparsers.add_parser(ACTION_LIST_PROJECTS,
                                        usage=f'{invoke_cmd}',
                                        epilog=f'Example: {invoke_cmd}\n\n',
                                        add_help=False)
    list_parser.add_argument('--help', action='store_true', help='show help')

    ###########################################################################
    #                           Link project parser                           #
    ###########################################################################

    link_parser = subparsers.add_parser(ACTION_LINK_PROJECT,
                                        usage=f'{invoke_cmd} [--help] [--name] PROJECT_NAME [--plugin] PROJECT_MANAGER',
                                        epilog=f'Example: {invoke_cmd} --name test_project --plugin fandanGO-cryoem-cnb  \n\n',
                                        add_help=False)
    link_parser.add_argument('--help', action='store_true', help='show help')
    link_parser.add_argument('--name', help='the name of the project to link\n')
    link_parser.add_argument('--plugin', help='the name of the plugin manager for the project (must be previously installed)\n')

    action_to_parser = {ACTION_CREATE_PROJECT: create_parser,
                        ACTION_DELETE_PROJECT: delete_parser,
                        ACTION_LIST_PROJECTS: list_parser,
                        ACTION_LINK_PROJECT: link_parser}
    parsed_args = parser.parse_args(sys.argv[1:])
    action = parsed_args.action
    parser_used = action_to_parser[action]
    exit_with_errors = False

    if parsed_args.help:
        parser_used.print_help()
        parser_used.exit(0)

    if action in ACTION_CREATE_PROJECT:
        if parsed_args.name:
            print('FandanGO will create a new project...')
            new_project = {'project_name': parsed_args.name,
                           'start_date': int(datetime.datetime.now().timestamp()),
                           'plugin_manager': None}
            create_new_project(new_project)
        else:
            print(f'Incorrect usage of command "{ACTION_CREATE_PROJECT}". Execute "{FANDANGO_CMD} {ACTION_CREATE_PROJECT} --help" or '
                  f'"{FANDANGO_CMD} --help" for more details')
            exit_with_errors = True

    elif action in ACTION_DELETE_PROJECT:
        if parsed_args.name:
            print('FandanGO will delete an existing project...')
            delete_project(parsed_args.name)
        else:
            print(f'Incorrect usage of command "{ACTION_DELETE_PROJECT}". Execute "{FANDANGO_CMD} {ACTION_DELETE_PROJECT} --help" or '
                  f'"{FANDANGO_CMD} --help" for more details')
            exit_with_errors = True

    elif action in ACTION_LIST_PROJECTS:
        column_names, projects = list_projects()
        print('FandanGO project list:\n')
        print(tabulate(projects, headers=column_names, tablefmt="pretty"))

    elif action in ACTION_LINK_PROJECT:
        if parsed_args.name and parsed_args.plugin:
            # check first if plugin is installed
            plugin_entry_point = entry_points().select(group='fandango.plugin', name=parsed_args.plugin)
            if plugin_entry_point:
                 update_project(parsed_args.name, 'plugin_manager', parsed_args.plugin)
            else:
                print(f"ERROR: Couldn't find entrypoint for plugin {parsed_args.plugin}. Looks like either is not installed or you misspelled the plugin name.")
                exit_with_errors = True
        else:
            print(f'Incorrect usage of command "{ACTION_LINK_PROJECT}". Execute "{FANDANGO_CMD} {ACTION_LINK_PROJECT} --help" or '
                  f'"{FANDANGO_CMD} --help" for more details')
            exit_with_errors = True

    if exit_with_errors:
        parser_used.exit(1)
    else:
        parser_used.exit(0)
