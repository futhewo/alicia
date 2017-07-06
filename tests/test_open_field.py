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
# Unit-tests of Alicia



# Imports #####################################################################
from nose.tools import *

from alicia.configuration import *
from alicia.open_field import *
from alicia.integer_content import *
from alicia.string_content import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass


# OpenField ###################################################################
def test_OpenField___init__():
    global elementId
    elementId = 0
    content0 = StringContent("ABCDE")
    element0 = OpenField(content0, 32)
    assert_equals(element0.elementId        , 0)
    assert_equals(element0.type             , "OpenField")
    assert_equals(element0.name             , "OpenField 0")
    assert_equals(element0.static           , False)
    assert_equals(element0.weight           , 1.0)
    assert_equals(element0.boundElements    , [])
    assert_equals(element0.notifiable       , True)
    assert_equals(element0.parsed           , False)
    assert_equals(element0.content          , content0)
    assert_equals(element0.minSize          , 0)
    assert_equals(element0.maxSize          , 32)

    content1 = IntegerContent(12345)
    element1 = OpenField(content1, 4, minSize=2, name="My OpenField", weight=2.0)
    assert_equals(element1.elementId        , 1)
    assert_equals(element1.type             , "OpenField")
    assert_equals(element1.name             , "My OpenField")
    assert_equals(element1.static           , False)
    assert_equals(element1.weight           , 2.0)
    assert_equals(element1.boundElements    , [])
    assert_equals(element1.notifiable       , True)
    assert_equals(element1.parsed           , False)
    assert_equals(element1.content          , content1)
    assert_equals(element1.minSize          , 2)
    assert_equals(element1.maxSize          , 4)

   
def test_OpenField_fieldFuzz():
    content0 = StringContent("AAAAABBBBBCCCCCDDDDDEEEEEFFFFFGGGGG")
    element0 = OpenField(content0, 64)
   
    # Adding 
    rand = random.Random(0) 
    element0.fieldFuzz(rand)
    assert_equals(element0.compose()          , "AAAAABBBBBCCCCCDDDDDEEEEE(FFFFFGGGGG")
    element0.clean()
 
    # All
    rand = random.Random(1) 
    element0.fieldFuzz(rand)
    assert_equals(element0.compose()          , "+AAAAABBBBCCCCDDDD+DGEEEEF;FFFGGEGG")
    element0.clean()


def test_OpenField_fuzz():
    content0 = StringContent("0123456789")
    element0 = OpenField(content0, 20, minSize=10)

    # Mutation 
    element0.fuzz(0)
    assert_equals(element0.compose()          , "01234:6789")
    element0.clean()
        
    # Content
    element0.fuzz(1)
    assert_equals(element0.compose()          , "||ping -b 255.255.25")
    element0.clean()
 
    # Swap and add
    element0.fuzz(2)
    assert_equals(element0.compose()          , "0D193456782")
    element0.clean()
 
    # Swap and add
    element0.fuzz(10)
    assert_equals(element0.compose()          , "012345789")

