#
# Actions (first argument given to FandanGO).
#

ACTION_HELP = 'help'
ACTION_INSTALL_PLUGIN = 'install-plugin'
ACTION_UNINSTALL_PLUGIN = 'uninstall-plugin'
ACTION_CREATE_PROJECT = 'create-project'
ACTION_DELETE_PROJECT = 'delete-project'
ACTION_LINK_PROJECT = 'link-project'
ACTION_COPY_DATA = 'copy-project'
ACTION_PIP = 'pip'

ACTION_GENERATE_METADATA = 'generate-metadata'
ACTION_SEND_METADATA = 'send-metadata'

CORE_ACTIONS = [ACTION_CREATE_PROJECT,
                ACTION_DELETE_PROJECT]

INSTALL_ACTIONS = [ACTION_INSTALL_PLUGIN,
                   ACTION_UNINSTALL_PLUGIN]

OTHER_PLUGIN_ACTIONS = [ACTION_LINK_PROJECT,
                        ACTION_COPY_DATA,
                        ACTION_GENERATE_METADATA,
                        ACTION_SEND_METADATA]

FANDANGO_CMD = 'fandanGO'

#
# DDBB
#

DBNAME = 'fandanGO-core.sqlite'
