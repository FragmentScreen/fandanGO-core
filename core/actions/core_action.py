import sys
import argparse
import datetime
from core.constants import ACTION_CREATE_PROJECT, ACTION_DELETE_PROJECT, FANDANGO_CMD
from core.db.sqlite_db import create_new_project, delete_project


def perform_core_action():
    """ Deals with core basic actions """

    invoke_cmd = FANDANGO_CMD + ' ' + sys.argv[1]

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(help=f'action "{ACTION_CREATE_PROJECT}" or "{ACTION_DELETE_PROJECT}"',
                                       dest='action',
                                       title='Action',
                                       description=f'available actions are "{ACTION_CREATE_PROJECT}" or "{ACTION_DELETE_PROJECT}"')

    ###########################################################################
    #                          Create project parser                          #
    ###########################################################################

    create_parser = subparsers.add_parser(ACTION_CREATE_PROJECT, formatter_class=argparse.RawTextHelpFormatter,
                                          usage=f'{invoke_cmd} [-h] [-n] project_name',
                                          epilog=f'Example: {invoke_cmd} -n 202404091  \n\n',
                                          add_help=False)
    create_parser.add_argument('-h', '--help', action='store_true', help='show help')
    create_parser.add_argument('-n', '--name', help='the name of the project to create\n')

    ###########################################################################
    #                          Delete project parser                          #
    ###########################################################################

    delete_parser = subparsers.add_parser(ACTION_DELETE_PROJECT, aliases=[ACTION_DELETE_PROJECT],
                                          formatter_class=argparse.RawTextHelpFormatter,
                                          usage=f'{invoke_cmd} [-h] [-n] project_name',
                                          epilog=f'Example: {invoke_cmd} -n 202404091  \n\n',
                                          add_help=False)
    delete_parser.add_argument('-h', '--help', action='store_true', help='show help')
    delete_parser.add_argument('-n', '--name', help='the name of the project to delete\n')

    action_to_parser = {ACTION_CREATE_PROJECT: create_parser,
                        ACTION_DELETE_PROJECT: delete_parser}
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
            new_project = {'project_id': parsed_args.name,
                           'start_date': int(datetime.datetime.now().timestamp()),
                           'proposal_manager': None,
                           'data_management_system': None,
                           'metadata_path': None}
            create_new_project(new_project)
        else:
            print('Incorrect usage of command "createpr". Execute "fandanGO createpr --help" or '
                  '"fandanGO --help" for more details')
            exit_with_errors = True

    elif action in ACTION_DELETE_PROJECT:
        if parsed_args.name:
            print('FandanGO will delete an existing project...')
            delete_project(parsed_args.name)
        else:
            print('Incorrect usage of command "deletepr". Execute "fandanGO deletepr --help" or '
                  '"fandanGO --help" for more details')
            exit_with_errors = True

    if exit_with_errors:
        parser_used.exit(1)
    else:
        parser_used.exit(0)
