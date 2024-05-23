from core.constants import ACTION_LINK_PROJECT, ACTION_COPY_DATA, ACTION_GENERATE_METADATA, ACTION_SEND_METADATA
from abc import ABC, abstractmethod


class Plugin(ABC):
    allowed_args = {}
    methods = {}

    @abstractmethod
    def define_args(cls):
        pass

    @classmethod
    def define_arg(cls, action_name, values):
        cls.allowed_args[action_name] = {**cls.allowed_args.get(action_name, {}), **values}

    @classmethod
    def get_args(cls):
        return cls.allowed_args

    @abstractmethod
    def define_methods(cls):
        pass

    @classmethod
    def define_method(cls, action_name, value):
        cls.methods[action_name] = value

    @classmethod
    def get_methods(cls):
        return cls.methods
