import sys
from core.constants import *

def get_mode():
    """ :returns the mode in which FandanGO has to be launched """
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return None

def main():
    mode = get_mode()

    if mode in INSTALL_ACTIONS:
        from core.actions.install_plugin import install_plugin_methods
        install_plugin_methods()

    elif mode in CORE_ACTIONS:
        from core.actions.core_action import perform_core_action
        perform_core_action()

    elif mode in OTHER_PLUGIN_ACTIONS:
        from core.actions.other_plugin_action import delegate_action_to_plugin
        delegate_action_to_plugin()

    # Else HELP or wrong argument
    else:
        sys.stdout.write(f'''\
Usage: fandanGO [ACTION] [ARGUMENTS]
                    
ACTION can be:
    {ACTION_HELP}\t\t\tPrints this help message.

    {ACTION_INSTALL_PLUGIN}\t\t\tInstalls FandanGO plugins.
    
    {ACTION_UNINSTALL_PLUGIN}\t\t\tUninstalls FandanGO plugins from a terminal.
    
    {ACTION_CREATE_PROJECT}\t\t\tCreates a FandanGO project.
    
    {ACTION_DELETE_PROJECT}\t\t\tDeletes a FandanGO project.
    
    {ACTION_COPY_DATA}\t\t\tCopies a FandanGO project into a data sharing environment.

    {ACTION_GENERATE_METADATA}\t\tGenerates metadata file for a FandanGO project.

    {ACTION_SEND_METADATA}\t\tSends metadata from a FandanGO project.
                         
''')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit('Error at main: %s\n' % e)
