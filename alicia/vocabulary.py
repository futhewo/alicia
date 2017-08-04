#!/usr/bin/python
# -*-  encoding: iso-8859-1 -*-



###############################################################################
# Copyright 2017 @fuzztheworld
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



###############################################################################
# Vocabulary aliases.



# Imports #####################################################################
import random

from alicia.static_field import *
from alicia.contents.content import *
from alicia.utils import *



# Vocabulary ##################################################################
def n(subElements, name=None, static=False, weight=1.0):
    """
        Node constructor.
    """
    return Node(subElements, name, static, weight)


def isf(value, size=4, signed=False, littleEndian=False, name=None, weight=1.0):
    """
        Integer Static Field constructor.
    """
    content = IntegerContent(value, size, signed, littleEndian)
    return StaticField(content, name, weight)


def scf(value, name=None, weight=1.0):
    """
        String Close Field constructor.
    """
    content = StringContent(value)
    return CloseField(content, name, weight)


