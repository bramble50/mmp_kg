# -*- coding: utf-8 -*-
"""

"""
import logging
from abc import ABC, abstractmethod


class ChemDb(ABC):
    logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)

    @abstractmethod
    def source_name(self):
        """ name of data source"""

    @abstractmethod
    def get_connection(self):
        """ Return a database python database interface for this database"""

    @abstractmethod
    def make_query(self, template, **kwargs):
        """ query the database using a predefined template and keyword args"""

    @abstractmethod
    def get_available_query_templates():
        """ Return available templates instantiated in query_template_dict"""