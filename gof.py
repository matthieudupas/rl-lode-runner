# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 07:59:44 2023

@author: Matthieu Dupas
"""


class Singleton(type):
    """Define a generic Singleton."""

    def __init__(self, *args, **kwargs):
        """Initializes."""
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Make the instance callable."""
        return self.get_instance(*args, **kwargs)
        # raise TypeError("Can't instantiate directly "+self.__name__)

    def get_instance(self, *args, **kwargs):
        """Get the unique instance."""
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
        return self.__instance


class ObjectFactory:
    """Defines a general purpose factory"""
    def __init__(self):
        """Initialize the factoty."""
        self._builders = {}

    def register_builder(self, key, builder):
        """Register a builder."""
        self._builders[key] = builder

    def create(self, key, **kwargs):
        """"Create and run the builder."""
        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder(**kwargs)