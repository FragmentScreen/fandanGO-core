#
# Actions (first argument given to FandanGO).
#

ACTION_HELP = 'help'

ACTION_INSTALL_PLUGIN = 'install-plugin'
ACTION_UNINSTALL_PLUGIN = 'uninstall-plugin'
ACTION_CREATE_PROJECT = 'create-project'
ACTION_DELETE_PROJECT = 'delete-project'
ACTION_LIST_PROJECTS = 'list-projects'
ACTION_LINK_PROJECT = 'link-project'
ACTION_PRINT_PROJECT = 'print-project'

ACTION_COPY_DATA = 'copy-data'
ACTION_GENERATE_METADATA = 'generate-metadata'
ACTION_SEND_METADATA = 'send-metadata'

ACTION_PIP = 'pip'

ACTION_EXECUTE = 'execute'

CORE_ACTIONS = [ACTION_CREATE_PROJECT,
                ACTION_DELETE_PROJECT,
                ACTION_LIST_PROJECTS,
                ACTION_LINK_PROJECT]

INSTALL_ACTIONS = [ACTION_INSTALL_PLUGIN,
                   ACTION_UNINSTALL_PLUGIN]

OTHER_PLUGIN_ACTIONS = [ACTION_EXECUTE]

FANDANGO_CMD = 'fandanGO'

#
# DDBB
#

DBNAME = 'fandanGO-core.sqlite'
