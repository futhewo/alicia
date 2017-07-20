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

from alicia.contents.string_content import *
from alicia.contents.integer_content import *
from alicia.static_field import *
from alicia.size_field import *
from alicia.padding_field import *
from alicia.node import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass


# SizeField ###################################################################
def test_SizeField___init__():
    content0 = IntegerContent(10)
    element0 = SizeField(content0, [])
    assert_equals(element0.type             , "SizeField")
    assert_equals(element0.static           , False)
    assert_equals(element0.weight           , 1.0)
    assert_equals(element0.boundElements    , [])
    assert_equals(element0.notifiable       , True)
    assert_equals(element0.parsed           , False)
    assert_equals(element0.content          , content0)
    assert_equals(element0.selfSize         , False)
    assert_equals(element0.elements         , [])
    assert_equals(content0.compose()        , "\x00\x00\x00\x00")

    content1 = StringContent("12345")
    element1 = OpenField(content1, 32, name="My ContentField")
    content2 = IntegerContent(0)
    element2 = SizeField(content2, [element1], selfSize=True, name="My SizeField", weight=2.5)
    assert_equals(element2.type             , "SizeField")
    assert_equals(element2.name             , "My SizeField")
    assert_equals(element2.static           , False)
    assert_equals(element2.weight           , 2.5)
    assert_equals(element2.boundElements    , [])
    assert_equals(element2.notifiable       , True)
    assert_equals(element2.parsed           , False)
    assert_equals(element2.content          , content2)
    assert_equals(element2.selfSize         , True)
    assert_equals(element2.elements         , [element1])
    assert_equals(content2.compose()        , "\x00\x00\x00\x09")
    assert_equals(element1.boundElements    , [element2])


def test_SizeField___str__():
    content0 = StringContent("ABCDE")
    content1 = IntegerContent(0)
    element0 = StaticField(content0, name="My StaticField")
    element1 = SizeField(content1, [element0], name="My SizeField")
    assert_equals(str(element1)             , "[My SizeField]: (False:4) [My StaticField]\n")


def test_SizeField_notify():
    content0 = StringContent("ABCDE")
    element0 = OpenField(content0, 32)

    content1 = IntegerContent(0)
    element1 = SizeField(content1, [element0])
    element1.notify()
    assert_equals(element1.compose()       , "\x00\x00\x00\x05")

    # Harder example
    content2 = StringContent("ABCDEFGHIJKLM")
    element2 = OpenField(content2, 32)
    content3 = StringContent("12345")
    element3 = OpenField(content3, 32)
    content4 = StringContent("#")
    element4 = PaddingField(content4, 8, [element0])
    node0 = Node([element2])
    node1 = Node([node0, element3])
    node2 = Node([element0, element4])
    node3 = Node([node1, node2])

    content5 = IntegerContent(0, littleEndian=True)
    element5 = SizeField(content5, [node3], selfSize=True)
    
    element5.notify()
    assert_equals(element5.compose()       , "\x1e\x00\x00\x00")
    

def test_SizeField_computeSize():
    content0 = StringContent("ABCDE")
    element0 = OpenField(content0, 32)

    content1 = IntegerContent(0)
    element1 = SizeField(content1, [element0])
    element1.notify()
    assert_equals(element1.computeSize()       , 5)

    # Harder example
    content2 = StringContent("ABCDEFGHIJKLM")
    element2 = OpenField(content2, 32)
    content3 = StringContent("12345")
    element3 = OpenField(content3, 32)
    content4 = StringContent("#")
    element4 = PaddingField(content4, 8, [element0])
    node0 = Node([element2])
    node1 = Node([node0, element3])
    node2 = Node([element0, element4])
    node3 = Node([node1, node2])

    content5 = IntegerContent(0, littleEndian=True)
    element5 = SizeField(content5, [node3], selfSize=True)
    
    element5.notify()
    assert_equals(element5.computeSize()       , 30)


def test_SizeField_notification():
    """
        A global test on the notification mechanism.
    """
    content0 = StringContent("ABCDE")
    element0 = OpenField(content0, 32)
    content1 = IntegerContent(0)
    element1 = SizeField(content1, [element0])
    content2 = StringContent("ABCDEFGHIJKLM")
    element2 = OpenField(content2, 32)
    content3 = StringContent("12345")
    element3 = OpenField(content3, 32)
    content4 = StringContent("#")
    element4 = PaddingField(content4, 8, [element0])
    node0 = Node([element2])
    node1 = Node([node0, element3])
    node2 = Node([element0, element4])
    node3 = Node([node1, node2])

    content5 = IntegerContent(0, littleEndian=True)
    element5 = SizeField(content5, [node3], selfSize=True)

    element0.update("1234567890")
    element2.update("A")

    assert_equals(element4.compose()            , "######")
    assert_equals(element5.compose()            , "\x1a\x00\00\x00")


