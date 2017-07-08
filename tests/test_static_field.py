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
from alicia.string_content import *
from alicia.integer_content import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass


# StaticField #################################################################
def test_StaticField___init__():
    content0 = StringContent("ABCDE")
    element0 = StaticField(content0)
    assert_equals(element0.type             , "StaticField")
    assert_equals(element0.static           , True)
    assert_equals(element0.weight           , 1.0)
    assert_equals(element0.boundElements    , [])
    assert_equals(element0.notifiable       , True)
    assert_equals(element0.parsed           , False)
    assert_equals(element0.content          , content0)

    content1 = IntegerContent(12345)
    element1 = StaticField(content1, name="My StaticField", weight=2.0)
    assert_equals(element1.type             , "StaticField")
    assert_equals(element1.name             , "My StaticField")
    assert_equals(element1.static           , True)
    assert_equals(element1.weight           , 2.0)
    assert_equals(element1.boundElements    , [])
    assert_equals(element1.notifiable       , True)
    assert_equals(element1.parsed           , False)
    assert_equals(element1.content          , content1)


def test_StaticField_getSize():
    content0 = StringContent("ABCDE")
    element0 = StaticField(content0)
    assert_equals(element0.getSize()       , 5)


def test_StaticField___str__():
    content0 = StringContent("ABCDE")
    element0 = StaticField(content0, name="My StaticField", weight=2.0)
    assert_equals(str(element0)             , "[My StaticField: ABCDE (StringContent)]\n")


def test_StaticField_compose():
    content0 = StringContent("ABCDE")
    element0 = StaticField(content0)
    assert_equals(element0.compose()       , "ABCDE") 


def test_StaticField_commit():
    content0 = StringContent("ABCDE")
    element0 = StaticField(content0)
    element0.content.future = "FGHEI"
    element0.commit()
    assert_equals(element0.compose()       , "FGHEI") 


def test_StaticField_clean():
    content0 = StringContent("ABCDE")
    element0 = StaticField(content0)
    element0.content.current = "FGHEI"
    element0.clean()
    assert_equals(element0.compose()       , "ABCDE")

