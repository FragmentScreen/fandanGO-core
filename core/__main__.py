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
        sys.stdout.write('''\
Usage: fandanGO [ACTION] [ARGUMENTS]
                    
ACTION can be:
    %s           Prints this help message.

    %s      Installs FandanGO plugins.
    
    %s    Uninstalls FandanGO plugins from a terminal.
    
    %s       Creates a FandanGO project.
    
    %s       Deletes a FandanGO project.
    
    %s         Copies a FandanGO project into a data sharing environment.
''' % (ACTION_HELP,
       ACTION_INSTALL_PLUGIN,
       ACTION_UNINSTALL_PLUGIN,
       ACTION_CREATE_PROJECT,
       ACTION_DELETE_PROJECT,
       ACTION_COPY_DATA
       ))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit('Error at main: %s\n' % e)
