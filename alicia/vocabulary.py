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

# Nodes ===============================
def n(subElements, name=None, static=False, weight=1.0):
    """
        Node constructor.
    """
    return Node(subElements, name, static, weight)


def c(subElements, name=None, static=False, weight=1.0):
    """
        Choice constructor.
    """
    return Choice(subElements, name, static, weight)


# Specials ============================
def cf(value, size, signed, littleEndian, element, name=None, weight=1.0):
    """
        Count Field constructor
    """
    content = IntegerContent(value, size, signed, littleEndian)
    return CountField(content, element, name, weight)

    
def sf(value, size, signed, littleEndian, elements, name=None, weight=1.0):
    """
        Count Field constructor
    """
    content = IntegerContent(value, size, signed, littleEndian)
    return SizeField(content, elements, name, weight)


# Binary ==============================
def bsf(value, name=None, weight=1.0):
    """
        Binary Static Field constructor.
    """
    content = BinaryContent(value)
    return StaticField(content, name, weight)


def bcf(value, name=None, weight=1.0):
    """
        Binary Close Field constructor.
    """
    content = BinaryContent(value)
    return CloseField(content, name, weight)


def bof(value, maxSize, minSize=0, name=None, weight=1.0):
    """
        Binary Open Field constructor.
    """
    content = BinaryContent(value)
    return OpenField(content, maxSize, minSize, name, weight)


def bpf(value, paddingSize, elements, name=None, weight=1.0):
    """
        Binary Padding Field constructor.
    """
    content = BinaryContent(value)
    return PaddingField(content, paddingSize, elements, name, weight)


# Careful ==============================
def csf(value, name=None, weight=1.0):
    """
        Careful Static Field constructor.
    """
    content = CarefulContent(value)
    return StaticField(content, name, weight)


def ccf(value, name=None, weight=1.0):
    """
        Careful Close Field constructor.
    """
    content = CarefulContent(value)
    return CloseField(content, name, weight)


def cof(value, maxSize, minSize=0, name=None, weight=1.0):
    """
        Careful Open Field constructor.
    """
    content = CarefulContent(value)
    return OpenField(content, maxSize, minSize, name, weight)


def cpf(value, paddingSize, elements, name=None, weight=1.0):
    """
        Careful Padding Field constructor.
    """
    content = CarefulContent(value)
    return PaddingField(content, paddingSize, elements, name, weight)


# Integer =============================
def isf(value, size=4, signed=False, littleEndian=False, name=None, weight=1.0):
    """
        Integer Static Field constructor.
    """
    content = IntegerContent(value, size, signed, littleEndian)
    return StaticField(content, name, weight)


def icf(value, size=4, signed=False, littleEndian=False, name=None, weight=1.0):
    """
        Integer Close Field constructor.
    """
    content = IntegerContent(value, size, signed, littleEndian)
    return CloseField(content, name, weight)


# String ==============================
def ssf(value, name=None, weight=1.0):
    """
        String Static Field constructor.
    """
    content = StringContent(value)
    return StaticField(content, name, weight)


def scf(value, name=None, weight=1.0):
    """
        String Close Field constructor.
    """
    content = StringContent(value)
    return CloseField(content, name, weight)


def sof(value, maxSize, minSize=0, name=None, weight=1.0):
    """
        String Open Field constructor.
    """
    content = StringContent(value)
    return OpenField(content, maxSize, minSize, name, weight)


def spf(value, paddingSize, elements, name=None, weight=1.0):
    """
        Careful Padding Field constructor.
    """
    content = StringContent(value)
    return PaddingField(content, paddingSize, elements, name, weight)
