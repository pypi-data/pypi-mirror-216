# -*- coding: utf-8 -*-
"""
.. :module:: imp-oasdiffgen
   :platform: Linux
   :synopsis: This service is bootstrapped by python-starter

   :copyright: (c) 2023 CloudVector, Inc. All rights reserved.
.. moduleauthor:: Imperva <engineering@imperva.com> (Jun 20, 2023)
"""

import os
import sys
from ._version import __version__

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
