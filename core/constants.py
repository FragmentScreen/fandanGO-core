#
# Actions (first argument given to FandanGO).
#

ACTION_HELP = 'help'
ACTION_INSTALL_PLUGIN = 'installpl'
ACTION_UNINSTALL_PLUGIN = 'uninstallpl'
ACTION_CREATE_PROJECT = 'createpr'
ACTION_DELETE_PROJECT = 'deletepr'
ACTION_COPY_DATA = 'copypr'

ACTION_GENERATE_METADATA = 'generate-metadata'
ACTION_SEND_METADATA = 'send-metadata'

CORE_ACTIONS = [ACTION_CREATE_PROJECT,
                ACTION_DELETE_PROJECT]

INSTALL_ACTIONS = [ACTION_INSTALL_PLUGIN,
                   ACTION_UNINSTALL_PLUGIN]

OTHER_PLUGIN_ACTIONS = [ACTION_COPY_DATA,
                        ACTION_GENERATE_METADATA,
                        ACTION_SEND_METADATA]

FANDANGO_CMD = 'fandanGO'

#
# DDBB
#

DBNAME = 'fandanGO-core.sqlite'
