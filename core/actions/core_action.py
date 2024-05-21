import sys
import argparse
import datetime
from core.constants import ACTION_CREATE_PROJECT, ACTION_DELETE_PROJECT, ACTION_LIST_PROJECTS, FANDANGO_CMD
from core.db.sqlite_db import create_new_project, delete_project, list_projects
from tabulate import tabulate

def perform_core_action():
    """ Deals with core basic actions """

    invoke_cmd = FANDANGO_CMD + ' ' + sys.argv[1]

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help=f'action "{ACTION_CREATE_PROJECT}", "{ACTION_DELETE_PROJECT}" or "{ACTION_LIST_PROJECTS}"',
                                       dest='action',
                                       title='Action',
                                       description=f'available actions are "{ACTION_CREATE_PROJECT}", "{ACTION_DELETE_PROJECT}" or "{ACTION_LIST_PROJECTS}"')

    ###########################################################################
    #                          Create project parser                          #
    ###########################################################################

    create_parser = subparsers.add_parser(ACTION_CREATE_PROJECT, formatter_class=argparse.RawTextHelpFormatter,
                                          usage=f'{invoke_cmd} [--help] [--name] project-name',
                                          epilog=f'Example: {invoke_cmd} --name test_project  \n\n',
                                          add_help=False)
    create_parser.add_argument('--help', action='store_true', help='show help')
    create_parser.add_argument('--name', help='the name of the project to create\n')

    ###########################################################################
    #                          Delete project parser                          #
    ###########################################################################

    delete_parser = subparsers.add_parser(ACTION_DELETE_PROJECT, aliases=[ACTION_DELETE_PROJECT],
                                          formatter_class=argparse.RawTextHelpFormatter,
                                          usage=f'{invoke_cmd} [--help] [--name] project-name',
                                          epilog=f'Example: {invoke_cmd} --name test_project  \n\n',
                                          add_help=False)
    delete_parser.add_argument('--help', action='store_true', help='show help')
    delete_parser.add_argument('--name', help='the name of the project to delete\n')

    ###########################################################################
    #                           List projects parser                          #
    ###########################################################################

    list_parser = subparsers.add_parser(ACTION_LIST_PROJECTS, aliases=[ACTION_LIST_PROJECTS],
                                          formatter_class=argparse.RawTextHelpFormatter,
                                          usage=f'{invoke_cmd}',
                                          epilog=f'Example: {invoke_cmd}\n\n',
                                          add_help=False)
    list_parser.add_argument('--help', action='store_true', help='show help')

    action_to_parser = {ACTION_CREATE_PROJECT: create_parser,
                        ACTION_DELETE_PROJECT: delete_parser,
                        ACTION_LIST_PROJECTS: list_parser}
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

    if exit_with_errors:
        parser_used.exit(1)
    else:
        parser_used.exit(0)
