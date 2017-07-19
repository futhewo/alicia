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

from alicia.string_content import *
from alicia.integer_content import *
from alicia.static_field import *
from alicia.count_field import *
from alicia.node import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass


# CountField ##################################################################
def test_CountField___init__():
    content0 = IntegerContent(10)
    node0 = Node([])
    element0 = CountField(content0, node0)
    assert_equals(element0.type             , "CountField")
    assert_equals(element0.static           , False)
    assert_equals(element0.weight           , 1.0)
    assert_equals(element0.boundElements    , [])
    assert_equals(element0.notifiable       , True)
    assert_equals(element0.parsed           , False)
    assert_equals(element0.content          , content0)
    assert_equals(element0.element          , node0)
    assert_equals(content0.compose()        , "\x00\x00\x00\x00")

    content1 = StringContent("12345")
    element1 = OpenField(content1, 32)
    node1 = Node([element1, element1, element1])
    content2 = IntegerContent(0)
    element2 = CountField(content2, node1, name="My CountField", weight=2.5)
    assert_equals(element2.type             , "CountField")
    assert_equals(element2.name             , "My CountField")
    assert_equals(element2.static           , False)
    assert_equals(element2.weight           , 2.5)
    assert_equals(element2.boundElements    , [])
    assert_equals(element2.notifiable       , True)
    assert_equals(element2.parsed           , False)
    assert_equals(element2.content          , content2)
    assert_equals(element2.element          , node1)
    assert_equals(content2.compose()        , "\x00\x00\x00\x03")
    assert_equals(node1.boundElements       , [element2])


def test_CountField___str__():
    content0 = StringContent("ABCDE")
    content1 = IntegerContent(0)
    element0 = StaticField(content0, name="My StaticField")
    element2 = Node([element0], name="My Node")
    element1 = CountField(content1, element2, name="My CountField")
    assert_equals(str(element1)             , "[My CountField]: (4) My Node [My StaticField]\n")


def test_CountField_notify():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    node0 = Node([element0, element0, element0])

    content1 = IntegerContent(0)
    element1 = CountField(content1, node0)
    element1.notify()
    assert_equals(element1.compose()       , "\x00\x00\x00\x03")

    # Harder example
    content2 = StringContent("ABCDE")
    content3 = StringContent("ABCDE")
    content4 = StringContent("ABCDE")
    content5 = StringContent("ABCDE")
    element2 = CloseField(content0)
    element3 = CloseField(content0)
    element4 = CloseField(content0)
    element5 = CloseField(content0)
    node1 = Node([element0, node0, element1, element2, element2, element3, element3, element3, element4, element4, element4, element4, element5, element5, element5, element5, element5])

    content6 = IntegerContent(0, littleEndian=True)
    element6 = CountField(content6, node1)
    
    element6.notify()
    assert_equals(element6.compose()       , "\x11\x00\x00\x00")
    

def test_CountField_computeCount():
    content0 = StringContent("ABCDE")
    element0 = CloseField(content0)
    node0 = Node([element0, element0, element0])

    content1 = IntegerContent(0)
    element1 = CountField(content1, node0)
    element1.notify()
    assert_equals(element1.computeCount()       , 3)

    # Harder example
    content2 = StringContent("ABCDE")
    content3 = StringContent("ABCDE")
    content4 = StringContent("ABCDE")
    content5 = StringContent("ABCDE")
    element2 = CloseField(content0)
    element3 = CloseField(content0)
    element4 = CloseField(content0)
    element5 = CloseField(content0)
    node1 = Node([element0, node0, element1, element2, element2, element3, element3, element3, element4, element4, element4, element4, element5, element5, element5, element5, element5])

    content6 = IntegerContent(0, littleEndian=True)
    element6 = CountField(content6, node1)
    
    element6.notify()
    assert_equals(element6.computeCount()       , 17)


