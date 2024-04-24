from core.constants import ACTION_COPY_DATA, ACTION_GENERATE_METADATA, ACTION_SEND_METADATA


class Plugin:
    allowed_args = {}
    methods = {}

    @classmethod
    def define_arg(cls, action_name, values):
        cls.allowed_args[action_name] = {**cls.allowed_args.get(action_name, {}), **values}

    @classmethod
    def define_args(cls):
        cls.define_arg(ACTION_COPY_DATA, {'n': {'long_name': 'project-name',
                                                'help': 'the name of the project to copy onto a data sharing environment',
                                                'required': True},
                                          'd': {'long_name': 'raw-data-path',
                                                'help': 'path of the raw data',
                                                'required': True}
                                          })

        cls.define_arg(ACTION_GENERATE_METADATA, {'n': {'long_name': 'project-name',
                                                        'help': 'the name of the project for which metadata will be generated',
                                                        'required': True}
                                                  })

        cls.define_arg(ACTION_SEND_METADATA, {'n': {'long_name': 'project-name',
                                                    'help': 'the name of the project for which metadata will be sent',
                                                    'required': True}
                                              })

    @classmethod
    def get_args(cls):
        return cls.allowed_args

    @classmethod
    def define_method(cls, action_name, value):
        cls.methods[action_name] = value

    @classmethod
    def get_methods(cls):
        return cls.methods
