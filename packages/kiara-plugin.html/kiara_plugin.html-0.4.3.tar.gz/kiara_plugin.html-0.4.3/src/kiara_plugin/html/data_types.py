# -*- coding: utf-8 -*-

"""This module contains the value type classes that are used in the ``kiara_plugin.html`` package.
"""
from kiara.data_types.included_core_types import StringType


class HtmlType(StringType):

    _data_type_name = "html"
