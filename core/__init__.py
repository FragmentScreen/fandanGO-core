from core.constants import ACTION_COPY_DATA


class Plugin:

    allowed_args = {}
    methods = {}

    @classmethod
    def define_arg(cls, action_name, values):
        cls.allowed_args[action_name] = {**cls.allowed_args.get(action_name, {}), **values}

    @classmethod
    def define_args(cls):
        cls.define_arg(ACTION_COPY_DATA, {'n': {'long_name': 'name',
                                               'help': 'the name of the project to copy onto a data sharing environment',
                                               'required': True},
                                          'd': {'long_name': 'raw_data_path',
                                                'help': 'path of the raw data',
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
