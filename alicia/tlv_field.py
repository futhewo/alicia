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
# Vocabulary structure, i.e. definition of fields and the structure that comes with it.



# Imports #####################################################################
import random
import string
import copy

from alicia.field import *
from alicia.size_field import *
from alicia.utils import *



# Field creators ###############################################################
def TLVFields(tValue, lSize, vValue, tValues=[], vValues=[], endianness="be", minValue=0, maxValue=0, name=None, fuzzing=None, overflowing=None, randoming=None, fuzzingNumber=None, overflowNumber=None, randomRate=None, randomNumber=None):
    """
        Create three fields forming a TLVField.
        @return [Field, SizeField, Field] the three created fields.
    """
    tName = None
    vName = None
    lName = None
    if name is not None:
        tName = "t" + name
        vName = "v" + name
        lName = "l" + name
    
    t = Field(tValue, 0, 0, tValues, tName, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber, randomRate, randomNumber)
    v = Field(vValue, 0, 256 ** lSize,  vValues, vName, fuzzing, overflowing, randoming, fuzzingNumber, overflowNumber,randomRate, randomNumber)
    l = SizeField([v], lSize, False, endianness, minValue, maxValue, lName, fuzzing, overflowing, randoming, fuzzingNumber,overflowNumber, randomRate, randomNumber)
    return [t, l, v]

