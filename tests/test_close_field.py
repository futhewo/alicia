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
from alicia.close_field import *
from alicia.integer_content import *
from alicia.string_content import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass


# Field #######################################################################
def test_CloseField___init__():
    global elementId
    elementId = 0
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    assert_equals(element0.elementId        , 0)
    assert_equals(element0.type             , "CloseField")
    assert_equals(element0.name             , "CloseField 0")
    assert_equals(element0.static           , False)
    assert_equals(element0.weight           , 1.0)
    assert_equals(element0.boundElements    , [])
    assert_equals(element0.notifiable       , True)
    assert_equals(element0.parsed           , False)
    assert_equals(element0.content          , content0)

    content1 = IntegerContent(12345)
    element1 = CloseField(content1, name="My CloseField", weight=2.0)
    assert_equals(element1.elementId        , 1)
    assert_equals(element1.type             , "CloseField")
    assert_equals(element1.name             , "My CloseField")
    assert_equals(element1.static           , False)
    assert_equals(element1.weight           , 2.0)
    assert_equals(element1.boundElements    , [])
    assert_equals(element1.notifiable       , True)
    assert_equals(element1.parsed           , False)
    assert_equals(element1.content          , content1)

   
def test_CloseField_update():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    element0.update("FGHIJ")
    assert_equals(element0.content.current  , "FGHIJ")


def test_CloseField_fieldFuzz():
    content0 = StringContent("AAAAABBBBBCCCCCDDDDDEEEEEFFFFFGGGGG")
    element0 = CloseField(content0)
   
    # Mutation 
    rand = random.Random(0) 
    element0.fieldFuzz(rand)
    assert_equals(element0.compose()          , "AAAAABBBBBCCCCCDDDDDEEEEE(FFFFGGGGG")
    element0.clean()
 
    # Swap and mutation 
    rand = random.Random(1) 
    element0.fieldFuzz(rand)
    assert_equals(element0.compose()          , "+AAAABBBBGCCC+CDDDDG;EEEEF<FFFBGDGG")
    element0.clean()


def test_CloseField_newFuzzedSubElement():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    rand = random.Random(0) 
    assert_equals(element0.newFuzzedSubElement(rand), "\\")
    
     

def test_CloseField_fuzz():
    content0 = IntegerContent(255, size=4)
    element0 = CloseField(content0)

    # Mutation 
    element0.fuzz(2)
    assert_equals(element0.compose()          , "\x00\x00\xfe\xff")
    element0.clean()
        
    # Swap 
    element0.fuzz(6)
    assert_equals(element0.compose()          , "\x00\xff\x00\x00")
    element0.clean()
 
    # Content 
    element0.fuzz(1)
    assert_equals(element0.compose()          , "\x00\x00\x00\x00")
 
