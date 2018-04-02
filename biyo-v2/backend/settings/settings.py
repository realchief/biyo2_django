# -*- coding: utf-8 -*-

from base_settings import *

try:
    from settings_local import *
except ImportError as e:
    pass
