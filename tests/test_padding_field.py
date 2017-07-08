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
from alicia.padding_field import *
from alicia.node import *
from alicia.utils import *



# Nose functions ##############################################################
def setup():
    pass

def teardown():
    pass


# PaddingField ################################################################
def test_PaddingField___init__():
    content0 = StringContent("#")
    element0 = PaddingField(content0, 32, [])
    assert_equals(element0.type             , "PaddingField")
    assert_equals(element0.static           , False)
    assert_equals(element0.weight           , 1.0)
    assert_equals(element0.boundElements    , [])
    assert_equals(element0.notifiable       , True)
    assert_equals(element0.parsed           , False)
    assert_equals(element0.content          , content0)
    assert_equals(element0.padder           , "#")
    assert_equals(element0.maxSize          , 32)
    assert_equals(element0.elements         , [])

    content1 = IntegerContent(12345)
    element1 = StaticField(content1, name="My StaticField")
    element2 = PaddingField(content0, 24, [element1], name="My PaddingField", weight=2.5)
    assert_equals(element2.type             , "PaddingField")
    assert_equals(element2.name             , "My PaddingField")
    assert_equals(element2.static           , False)
    assert_equals(element2.weight           , 2.5)
    assert_equals(element2.boundElements    , [])
    assert_equals(element2.notifiable       , True)
    assert_equals(element2.parsed           , False)
    assert_equals(element2.content          , content0)
    assert_equals(element2.padder           , "#")
    assert_equals(element2.maxSize          , 24)
    assert_equals(element2.elements         , [element1])
    assert_equals(content0.compose()        , "#" * 20)
    assert_equals(element1.boundElements    , [element2])


def test_PaddingField___str__():
    content0 = StringContent("#")
    content1 = IntegerContent(12345)
    element0 = StaticField(content1, name="My StaticField")
    element1 = PaddingField(content0, 24, [element0], name="My PaddingField")
    assert_equals(str(element1)             , "[My PaddingField]: (#:24) [My StaticField]\n")


def test_PaddingField_notify():
    content0 = StringContent("#")
    content1 = IntegerContent(12345)
    element0 = StaticField(content1)
    element1 = PaddingField(content0, 8, [element0])
    element1.notify()
    assert_equals(element1.compose()       , "####")

    # Harder example
    content2 = StringContent("ABCDEF")
    content3 = IntegerContent(32)
    element2 = CloseField(content2)
    element3 = CloseField(content3)
    node0 = Node([element2])
    node1 = Node([node0, element3])
    node2 = Node([element0, element1])
    node3 = Node([node1, node2])

    content4 = StringContent("#")
    element4 = PaddingField(content4, 8, [node3])
    element4.notify()
    assert_equals(element4.compose()       , "######")


def test_PaddingField_computeSize():
    content0 = StringContent("#")
    content1 = IntegerContent(12345)
    element0 = StaticField(content1)
    element1 = PaddingField(content0, 8, [element0])
    assert_equals(element1.computeSize()   , 4) 


    # Harder example
    content2 = StringContent("ABCDEF")
    content3 = IntegerContent(32)
    element2 = CloseField(content2)
    element3 = CloseField(content3)
    node0 = Node([element2])
    node1 = Node([node0, element3])
    node2 = Node([element0, element1])
    node3 = Node([node1, node2])

    content4 = StringContent("#")
    element4 = PaddingField(content4, 8, [node3])
    element4.notify()
    assert_equals(element4.computeSize()       , 6)

