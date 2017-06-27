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
from alicia.static_field import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass


# Field #######################################################################
def test_StaticField___init__():
    global elementId
    elementId = 0
    element0 = StaticField("ABCDE")
    assert_equals(element0.elementId        , 0)
    assert_equals(element0.type             , "StaticField")
    assert_equals(element0.name             , "StaticField 0")
    assert_equals(element0.static           , True)
    assert_equals(element0.weight           , 1.0)
    assert_equals(element0.boundElements    , [])
    assert_equals(element0.notifiable       , True)
    assert_equals(element0.parsed           , False)
    assert_equals(element0.default          , "ABCDE")
    assert_equals(element0.current          , "ABCDE")
    assert_equals(element0.future           , "ABCDE")
    assert_equals(element0.content          , None)

    content0 = Content()
    element1 = StaticField("ABCDE", content=content0, name="My StaticField", weight=2.0)
    assert_equals(element1.elementId        , 1)
    assert_equals(element1.type             , "StaticField")
    assert_equals(element1.name             , "My StaticField")
    assert_equals(element1.static           , True)
    assert_equals(element1.weight           , 2.0)
    assert_equals(element1.boundElements    , [])
    assert_equals(element1.notifiable       , True)
    assert_equals(element1.parsed           , False)
    assert_equals(element1.default          , "ABCDE")
    assert_equals(element1.current          , "ABCDE")
    assert_equals(element1.future           , "ABCDE")
    assert_equals(element1.content.type     , "Content")

   
def test_StaticField___str__():
    element0 = StaticField("ABCDE", content="TEST", name="My StaticField", weight=2.0)
    assert_equals(str(element0)             , "[My StaticField: ABCDE (TEST)]\n")


def test_StaticField_compose():
    element0 = StaticField("ABCDE")
    assert_equals(element0.compose()       , "ABCDE") 


def test_StaticField_commit():
    element0 = StaticField("ABCDE")
    element0.future = "FGHEI"
    element0.commit()
    assert_equals(element0.current         , "FGHEI") 


def test_StaticField_clean():
    element0 = StaticField("ABCDE")
    element0.current = "FGHEI"
    element0.clean()
    assert_equals(element0.current         , "ABCDE")
 
